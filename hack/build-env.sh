#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

# This script may be called with `source`, so we can't rely on the `$0` trick.
PARENT_FOLDER=$(dirname "$BASH_SOURCE")

if [ "$#" -ne 3 ]; then
  echo 'Invalid number of arguments'
  echo "Usage: ./build-env.sh <srcFolder>"
  exit 1
fi

_installRequirements() {
  local _requirementsTxt=$1

  if ! [[ -f $_requirementsTxt ]]; then
    echo "Requirements not found at '$_requirementsTxt'"
    return
  fi

  echo "---> Found custom requirements.txt at $_requirementsTxt"
  pip3 install -r $_requirementsTxt --trusted-host $2 --extra-index-url $3
}

_generateDotenv() {
  local _srcFolder=$1
  local _dotenv=$2

  echo "---> Generating and sourcing default environment variables"
  local _generate_dotenv="$PARENT_FOLDER/generate_dotenv.py"
  $_generate_dotenv $_srcFolder $_dotenv
}

_main() {
  local _srcFolder=$1
  local _PIP_TRUSTED_HOST=$2
  local _PIP_EXTRA_INDEX_URL=$3

  local _requirementsTxt="$_srcFolder/requirements.txt"
  _installRequirements $_requirementsTxt $_PIP_TRUSTED_HOST $_PIP_EXTRA_INDEX_URL

  local _dotenv="./.env"
  _generateDotenv $_srcFolder $_dotenv

  # TODO: If MLServer is not present, should we install it from the local wheel
  # in the Docker image?
}

_main $1 $2 $3
