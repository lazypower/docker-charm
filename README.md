# Docker ![](https://d3oypxn00j2a10.cloudfront.net/0.12.10/img/nav/docker-logo-loggedout.png)



This charm provides [Docker](http://docker.io). Docker is an open platform for
developers and sysadmins to build, ship, and run distributed applications.
Consisting of Docker Engine, a portable, lightweight runtime and packaging tool,
and Docker Hub, a cloud service for sharing applications and automating
workflows, Docker enables apps to be quickly assembled from components and
eliminates the friction between development, QA, and production environments


# Using the Docker Charm

Step by step instructions on using the docker charm:

    juju deploy cs:~hazmat/trusty/flannel
    juju deploy cs:~lazypower/trusty/docker --to 1

## Scale out Usage

Scaling out the docker service is as simple as adding additional flannel units
and docker services to expand your cluster. Docker containers can be run on any
host and communicate with one another so long as the docker charm is co-located
with flannel.

## Known Limitations and Issues

The Docker charm currently *has* to be deployed in tandem with flannel to
communicate across the network with other docker containers. In any HA
configuration this will be a requirement.

# Configuration

- latest : By default the charm assumes installation from the ubuntu
repositories. If you wish to deploy the latest upstream docker runtime enable
this option.

# Contact Information

- Author: Charles Butler &lt;[charles.butler@ubuntu.com](mailto:charles.butler@ubuntu.com)&gt;

## Docker Upstream

- [Docker website](http://docker.io)
- [Docker bug tracker](http://github.com/docker/docker/issues)
- [Docker users mailing list](https://groups.google.com/forum/?fromgroups#!forum/docker-users)
- [Docker dev mailing list](https://groups.google.com/forum/?fromgroups#!forum/docker-dev)
