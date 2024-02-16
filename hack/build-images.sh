#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

ROOT_FOLDER="$(dirname "${0}")/.."
IMAGE_NAME="jioaicr.azurecr.io/jioai/vision/model/mlserver-python38-gpu"

#if [ "$#" -ne 4 ]; then
#  echo 'Invalid number of arguments'
#  echo "Usage: ./build-images.sh <version>"
#  exit 1
#fi

_buildImage() {
  local _runtimes=$1
  local _version=$2
  local _tag=$3
  local _git_commit=$4

  if [ "$#" -ne 5 ]; then
    local _http_proxy=""
    local _https_proxy=""
  else
    local _http_proxy=$5
    local _https_proxy=$6
  fi

  DOCKER_BUILDKIT=1 docker build $ROOT_FOLDER \
    --build-arg RUNTIMES="$_runtimes" \
    --build-arg GIT_COMMIT=$_git_commit \
    --build-arg VERSION=$_version \
    --build-arg http_proxy=$_http_proxy \
    --build-arg https_proxy=$_https_proxy \
    -t "$IMAGE_NAME:$_tag"
}

_buildRuntimeImage() {
  local _runtimePath=$1
  local _version=$2
  local _runtimeName=$(basename $_runtimePath)

  echo "---> Building MLServer runtime image: $_runtimeName"
  _buildImage "mlserver-$_runtimeName" "$_version-$_runtimeName"
}

_main() {
  local _version=$1

  echo "---> Building core MLServer images"
  #_buildImage "all" $_version

  if [ "$#" -ne 3 ]; then
    _buildImage "" $_version $_version-slim $2
  elif [ "$#" -ne 5 ]; then
    _buildImage "" $_version $_version-slim $2 $3 $4
  else
    echo "Usage: ./build-images.sh <version>"
    exit 1
  fi
  #for _runtimePath in "$ROOT_FOLDER/runtimes/"*; do
  #  _buildRuntimeImage $_runtimePath $_version
  #done
}

if [ "$#" -ne 3 ]; then
  _main $1 $2
elif [ "$#" -ne 5 ]; then
  _main $1 $2 $3 $4
else
  echo "Usage: ./build-images.sh <version>"
  exit 1
fi