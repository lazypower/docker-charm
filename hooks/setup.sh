#!/bin/bash
set -e

apt-get install -y \
    python-dev \
    python-pip \
    git \

pip install -r hooks/python-pkgs.txt


