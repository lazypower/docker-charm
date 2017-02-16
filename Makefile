#!/usr/bin/make

build: lint unit_test

virtualenv:
	virtualenv .venv

release: check-path virtualenv
	@.venv/bin/pip install git-vendor
	@.venv/bin/git-vendor sync -d ${DOCKER_MASTER_BZR}

check-path:
ifndef DOCKER_MASTER_BZR
	$(error DOCKER_MASTER_BZR is undefined)
endif

.PHONY: apt_prereqs
apt_prereqs:
	@# Need tox, but don't install the apt version unless we have to (don't want to conflict with pip)
	@which tox >/dev/null || (sudo apt-get install -y python-pip && sudo pip install tox)

.PHONY: lint
lint: apt_prereqs
	@tox --notest
	@charm proof

.PHONY: unit_test
unit_test: apt_prereqs
	@echo Starting tests...
	tox

clean:
	@rm -rf .venv
	@rm -rf .tox
	@find -name *.pyc -delete
