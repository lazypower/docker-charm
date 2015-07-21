#!/usr/bin/make

build: tox lint test

tox:
/usr/bin/tox:
	sudo apt-get install -y  python-tox python-dev python-virtualenv

lint: tox
	tox -e lint


unit_test: tox
	tox

release: check-path virtualenv
	@.venv/bin/pip install git-vendor
	@.venv/bin/git-vendor sync -d ${DOCKER_MASTER_BZR}

check-path:
ifndef DOCKER_MASTER_BZR
	$(error DOCKER_MASTER_BZR is undefined)
endif


clean:
	@rm -rf .venv
	@rm -rf .tox
	@find -name *.pyc -delete
