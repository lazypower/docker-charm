#!/bin/bash
set -e

apt-get install -y \
    python-dev \
    python-pip \
    git \

easy_install -U pip # hacky workaround
pip install -r hooks/python-pkgs.txt
