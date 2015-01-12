#!/usr/bin/make

build: virtualenv lint test

virtualenv: .venv/bin/python
.venv/bin/python:
	sudo apt-get install python-virtualenv
	virtualenv .venv
	.venv/bin/pip install nose flake8 mock pyyaml charmhelpers charm-tools ecdsa

lint:
	@.venv/bin/flake8 hooks unit_tests
	@ansible-playbook --syntax-check playbooks/site.yaml
	@.venv/bin/ansible-lint playbooks/site.yaml
	@.venv/bin/charm proof

unit_test: .venv/bin/python
	@echo Starting tests...
	@CHARM_DIR=. PYTHONPATH=./hooks .venv/bin/nosetests -vv --nologcapture unit_tests

func_test:
	@echo functional tests...
	@juju test 

clean:
	rm -rf .venv
	find -name *.pyc -delete
