# include .mk

SHELL=/bin/bash

define ASCILOGO
boss-ansible-homelab
=======================================
endef

export ASCILOGO

# http://misc.flogisoft.com/bash/tip_colors_and_formatting

RED=\033[0;31m
GREEN=\033[0;32m
ORNG=\033[38;5;214m
BLUE=\033[38;5;81m
NC=\033[0m

export RED
export GREEN
export NC
export ORNG
export BLUE

# verify that certain variables have been defined off the bat
check_defined = \
    $(foreach 1,$1,$(__check_defined))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $(value 2), ($(strip $2)))))

list_allowed_args  := name inventory

mkfile_path        := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir        := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))

PR_SHA             := $(shell git rev-parse HEAD)
REPO_ORG           := bossjones
REPO_NAME          := boss-quart-asyncio-lab
REPO_SLUG          := $(REPO_ORG)/$(REPO_NAME)
IMAGE_TAG          := $(REPO_SLUG):$(PR_SHA)
TEST_IMAGE_NAME    := $(IMAGE_TAG)
CONTAINER_NAME     := $(shell echo -n $(IMAGE_TAG) | openssl dgst -sha1 | sed 's/^.* //'  )
MKDIR              = mkdir


help:
	@printf "\033[1m$$ASCILOGO $$NC\n"
	@printf "\033[21m\n\n"
	@printf "=======================================\n"
	@printf "\n"

.PHONY: list
list:
	@$(MAKE) -qp | awk -F':' '/^[a-zA-Z0-9][^$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print A[i]}' | sort

.PHONY: yamllint-role
yamllint-role:
	bash -c "find .* -type f -name '*.y*ml' -print0 | xargs -I FILE -t -0 -n1 yamllint FILE"

# # NOTE: This assumes that all of your repos live in the same workspace!
# link_modulesets:
# 	# add aliases for dotfiles
# 	@for file in $(shell find $(CURDIR)/modulesets -name "*scarlett*modules" -print); do \
# 		echo $$file; \
# 		f=$$(basename $$file); \
# 		cp -fv $$file $$HOME/jhbuild/modulesets/$f; \
# 	done; \
# 	ls -lta $$HOME/jhbuild/modulesets/$f; \

# render_jhbuildrc:
# 	@scripts/render_jhbuild.py --cmd render

# docker_run:
# 	.ci/docker-run.sh

# bootstrap: jhbuild_bootstrap render link_modulesets jhbuild_list

# jhbuild_bootstrap:
# 	python scripts/render_jhbuild.py --cmd bootstrap

# compile_jhbuild:
# 	python scripts/render_jhbuild.py --cmd compile

# render:
# 	python scripts/render_jhbuild.py --cmd render

# jhbuild_list:
# 	jhbuild list

# pip-deps:
# 	pip install --upgrade pip && pip install pygobject==3.28.3 ptpython black isort ipython pdbpp Pillow matplotlib numpy_ringbuffer MonkeyType autopep8 pylint flake8 pytest

# create-full-local-hierachy:
# 	bash scripts/create-full-local-hierachy.sh

# clone-sphinx:
# 	python scripts/render_jhbuild.py --cmd clone-one --pkg sphinx

# mv-sphinx:
# 	mv -fv ~/gnome/* ~/src/

# dev-env: pip-deps create-full-local-hierachy clone-sphinx mv-sphinx

download-roles:
	ansible-galaxy install -r requirements.yml --roles-path ./roles/

# Compile python modules against homebrew openssl. The homebrew version provides a modern alternative to the one that comes packaged with OS X by default.
# OS X's older openssl version will fail against certain python modules, namely "cryptography"
# Taken from this git issue pyca/cryptography#2692
install-virtualenv-osx:
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install -r requirements.txt
