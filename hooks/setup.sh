#!/bin/bash
set -e

apt-get update

apt-get install -y \
    python-dev \
    python-pip \
    git

easy_install -U pip
