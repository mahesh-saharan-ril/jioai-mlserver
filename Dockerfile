FROM python:3.8-slim AS wheel-builder
SHELL ["/bin/bash", "-l", "-c"]

COPY ./hack/build-wheels.sh ./hack/build-wheels.sh
COPY ./jioai_mlserver ./jioai_mlserver
COPY ./runtimes ./runtimes
COPY \
    setup.py \
    README.md \
    ./

# This will build the wheels and place will place them in the
# /opt/mlserver/dist folder
RUN ./hack/build-wheels.sh /opt/mlserver/dist

#RUN file="$(ls /opt/mlserver/dist)" && echo $file

FROM nvidia/cuda:11.2.2-base-ubi8
SHELL ["/bin/bash", "-c"]

ARG PYTHON_VERSION=3.8.13
ARG CONDA_VERSION=4.13.0
ARG MINIFORGE_VERSION=${CONDA_VERSION}-1
ARG RUNTIMES="all"
ARG VERSION="NA" 
ARG http_proxy=""
ARG https_proxy=""

ENV MLSERVER_MODELS_DIR=/mnt/models \
    MLSERVER_ENV_TARBALL=/mnt/models/environment.tar.gz \
    MLSERVER_PATH=/opt/mlserver \
    CONDA_PATH=/opt/conda \
    PATH=/opt/mlserver/.local/bin:/opt/conda/bin:$PATH \
    https_proxy=http://prodproxy.jio.com:8080 \ 
    http_proxy=http://prodproxy.jio.com:8080

RUN dnf makecache --refresh
RUN dnf -y install microdnf

RUN yum module install -y llvm-toolset
RUN yum install -y cmake

# Install some base dependencies required for some libraries
RUN microdnf update -y && \
    microdnf install -y \
        tar \
        gzip \
        libgomp \
        mesa-libGL \
        glib2-devel \
        shadow-utils

# Install Conda, Python 3.8 and FFmpeg
RUN microdnf install -y wget && \
    wget "https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-x86_64.sh" \
        -O miniforge3.sh && \
    bash "./miniforge3.sh" -b -p $CONDA_PATH && \
    rm ./miniforge3.sh && \
    echo $PATH && \
    conda install --yes \
        python=$PYTHON_VERSION \
        ffmpeg && \
    conda clean -tipy && \
    microdnf remove -y wget && \
    echo "conda activate base" >> "$CONDA_PATH/etc/profile.d/conda.sh" && \
    ln -s "$CONDA_PATH/etc/profile.d/conda.sh" /etc/profile.d/conda.sh && \
    echo ". $CONDA_PATH/etc/profile.d/conda.sh" >> ~/.bashrc

RUN mkdir $MLSERVER_PATH
WORKDIR /opt/mlserver

# Create user and fix permissions
# NOTE: We need to make /opt/mlserver world-writable so that the image is
# compatible with random UIDs.
RUN useradd -u 1000 -s /bin/bash mlserver -d $MLSERVER_PATH && \
    chown -R 1000:0 $MLSERVER_PATH && \
    chmod -R 776 $MLSERVER_PATH

COPY --from=wheel-builder /opt/mlserver/dist ./dist

#RUN file="$(ls .)" && echo $file

# NOTE: if runtime is "all" we install mlserver-<version>-py3-none-any.whl
# we have to use this syntax to return the correct file: $(ls ./dist/mlserver-*.whl)
# NOTE: Temporarily excluding mllib from the main image due to:
#   CVE-2022-25168
#   CVE-2022-42889
RUN . $CONDA_PATH/etc/profile.d/conda.sh && \
    pip install --upgrade pip wheel setuptools && \
    if [[ $RUNTIMES == "all" ]]; then \
        for _wheel in "./dist/mlserver_"*.whl; do \
            if [[ ! $_wheel == *"mllib"* ]]; then \
                echo "--> Installing $_wheel..."; \
                pip install $_wheel; \
            fi \
        done \
    else \
        for _runtime in $RUNTIMES; do \
            _wheelName=$(echo $_runtime | tr '-' '_'); \
            _wheel="./dist/$_wheelName-"*.whl; \
            echo "--> Installing $_wheel..."; \
            pip install $_wheel; \
        done \
    fi && \
    pip install ./dist/jioai_mlserver-${VERSION}-py3-none-any.whl

COPY ./licenses/license.txt ./
COPY ./licenses/license.txt /licenses/
COPY \
    ./hack/build-env.sh \
    ./hack/generate_dotenv.py \
    ./hack/activate-env.sh \
    ./hack/

USER 1000

# add meta-information
ARG GIT_COMMIT=unspecified
LABEL git_commit=$GIT_COMMIT

# We need to build and activate the "hot-loaded" environment before MLServer
# starts
CMD . $CONDA_PATH/etc/profile.d/conda.sh && \
    source ./hack/activate-env.sh $MLSERVER_ENV_TARBALL && \
    mlserver start $MLSERVER_MODELS_DIR
