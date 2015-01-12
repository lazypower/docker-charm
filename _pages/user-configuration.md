---
layout: default
title: Configuration
category: User Docs
permalink: /user/configuration.html
---

# Configuration Options

##### latest

Type: Boolean

Deploys latest docker from the upstream repositories. Fetches the GPG key, and adds the docker
maintained repository to the apt sources list. Swaps package installation from `docker.io` to
`lxc-docker`

# Configuration Through Relations

The docker charm can reconfigure aspects of it self through different relationships exposed in
the `metadata.yaml` file. To date, there is only 1 relationship that will reconfigure the service
for [cross-host networking](#overlay-network).

## Exposed Interfaces

##### Relationship: docker-containers

##### Interface: containers

> Not currently implemented

This interface is presently unused - but is intended for broadcasting information about the running
containers on the host. Such information would include:

 - Container Name
 - Container Hash
 - Mapped Ports

This interface is exposed and intended to aid in consuming services that will be managing the
containers on the host, such as [Flocker](https://github.com/clusterhq/flocker) or
[Kubernetes](https://github.com/googlecloudplatform/kubernetes).

## Consumed Interfaces

##### Relationship: network

##### Interface: overlay-network

> Exists in: Experimental / Development branch

This interface is consumed to reconfigure the docker0 bridge that is created during boot of the
docker service. This is useful when you need to expose the containers to another network without
occupying the host-bridge port mapping.

##### Expected Data

- flannel-subnet
- flannel-mtu


