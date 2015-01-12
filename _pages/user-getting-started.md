---
layout: default
title: Getting Started
category: User Docs
permalink: /user/getting-started.html
---

# Getting Started

### Deploying The Stable Charm

> The docker charm is not presently in the charm store
> these instructions are pending a full charm review and
> charm-store acceptance.

    juju deploy cs:trusty/docker


### Deploying The Development Charm

    mkdir -p ~/charms/trusty
    export JUJU_REPOSITORY=$HOME/charms
    git clone https://github.com/chuckbutler/docker-charm.git charms/trusty/docker
    juju deploy local:trusty/docker


### Known Limitations


