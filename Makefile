# define vartiables required in Makefile.core
SHELL := $(shell which bash)
APP_PROJECT_NAME ?= jioai-mlserver
APP_CONDA_ENV_NAME ?= venv-$(APP_PROJECT_NAME)
APP_BUILD_ENV ?= dev

# define vartiables required in this Makefile
DOCKER_REPO ?= nexus.rjil.ril.com:5101
DOCKER_USERNAME ?= scm
DOCKER_PASSWORD ?= NA

APP_DEVEL_DOCKER_BASE_IMAGE := continuumio/miniconda3:latest
APP_DEVEL_DOCKER_IMAGE := devel/package/$(APP_PROJECT_NAME):latest

CONTAINER_REGISTRY_TYPE ?= azure-aicr

# include Makefile.core
include Makefile.core

AICR_DOCKER_REPO ?= jioaicr.azurecr.io
AICR_DOCKER_USERNAME ?= c2904d76-9dcb-4315-92ab-07610f612d7f
AICR_DOCKER_PASSWORD ?= NA 


# name devel docker image
APP_DEVEL_DOCKER_BASE_IMAGE_STRING := $(DOCKER_REPO_PATH)$(DOCKER_USERNAME_PATH)$(APP_DEVEL_DOCKER_BASE_IMAGE)
APP_DEVEL_DOCKER_IMAGE_STRING := $(DOCKER_REPO_PATH)$(DOCKER_USERNAME_PATH)$(APP_DEVEL_DOCKER_IMAGE)

package:
ifeq ($(CONTAINER_REGISTRY_TYPE), azure-aicr)
	$(MAKE) package-python-aicr
else
	$(MAKE) package-python-nexus
endif


package-python-nexus:
	@echo "Packaging disabled in this pipeline"

package-python-aicr:
	rm -rf ./{build,dist,*.egg-info}
	rm -rf ./**/*.egg-info
	$(CONDA_ACTIVATE) ./hack/build-wheels.sh ./dist


publish: 
ifeq ($(CONTAINER_REGISTRY_TYPE), azure-aicr)
	$(MAKE) publish-python-aicr
else
	$(MAKE) publish-python-nexus
endif

publish-python-aicr:
ifneq ($(TWINE_UPLOAD_REPOSITORY),)
	@echo "Publishing to $(TWINE_UPLOAD_REPOSITORY)"
	$(CONDA_ACTIVATE) python -m twine upload --verbose -p $(TWINE_UPLOAD_PASSWORD) -u $(TWINE_UPLOAD_USERNAME) --repository $(TWINE_UPLOAD_REPOSITORY) --repository-url $(TWINE_UPLOAD_REPOSITORY_URL) dist/*.whl
else
	$(error TWINE_UPLOAD_REPOSITORY not set)
endif

publish-python-nexus:
	@echo "Publishing disabled in this pipeline"

