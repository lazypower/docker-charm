# Docker ![](https://d3oypxn00j2a10.cloudfront.net/0.12.10/img/nav/docker-logo-loggedout.png)

[![Build Status](http://drone.dasroot.net/api/badge/github.com/chuckbutler/docker-charm/status.svg?branch=master)](http://drone.dasroot.net/github.com/chuckbutler/docker-charm)


This charm provides [Docker](http://docker.io). Docker is an open platform for
developers and sysadmins to build, ship, and run distributed applications.
Consisting of Docker Engine, a portable, lightweight runtime and packaging tool,
and Docker Hub, a cloud service for sharing applications and automating
workflows, Docker enables apps to be quickly assembled from components and
eliminates the friction between development, QA, and production environments


# Did you know?

There's a full documentation site that serves as a manual/accompanyment to this charm.
have a look at the [Github Pages Docsite](http://chuckbutler.github.com/docker-charm)
for more in-depth information about the charm, development patterns, and usage
instructions.

# Using the Docker Charm

Step by step instructions on using the docker charm:

    juju deploy cs:~lazypower/trusty/docker

## Scale out Usage

Scaling out the docker service is as simple as adding additional docker units
to expand your cluster. However, you will need an SDN solution to provide cross
host networking. See the Known Limitations and issues about this.

# Configuration

- latest : By default the charm assumes installation from the ubuntu
repositories. If you wish to deploy the latest upstream docker runtime enable
this option.

- version : String representation of the version you wish to deploy. This helps
    when scaling a cluster post deployment, to ensure you dont have mismatched
    versions deployed due to a new release

    juju set docker version=1.6.2

- compose : Boolean representtion on if you wish to include `docker compose`
    to be installed during the installation of `docker`. This allows you to
    leverage a yaml file to spin up and manage multiple containers that
    comprise a single application stack.

- aufs : **new as of v0.1.6** Defaults the backend storage driver to AUFS. The
    older option of device mapper was horribly broken in most setups, and has
    been completely depreciated by the Docker foundation. Disable to keep the
    DeviceMapper backend. - Not recommended. **note** this will break existing
    containers if you upgrade existing setups. Ensure you account for this when
    upgrading your docker clusters that are previously deployed with this charm.

    > See blurb under Known Issues for migration instructions.

## Known Limitations and Issues


#### AWS t1.micro

Performance will suffer on an AWS t1.micro unit - as it has such a limited amount of ram. Between
the juju unit-agent, and the docker daemon + workloads - you will only be able to run the smallest
of deployments on them. Thus it is not recommended.

#### Local Provider Blockers

 The Docker Charm will not work out of the box on the
 [local provider](https://jujucharms.com/docs/config-local). LXC containers are goverend by a
 very strict [App Armor](https://wiki.ubuntu.com/AppArmor)
 [policy](https://help.ubuntu.com/lts/serverguide/lxc.html#lxc-apparmor) that prevents accidental
 misuses of privilege inside the container. Thus **running the Docker Charm inside the local provider
 is not a supported deployment method**.

 Additional information will be made available after more research has been done on enabling the
 Docker charm to be deployed into a LXC container environment, and while unsupported it will
 outline the process to enable such scenarios for users that wish to test on the local provider.

#### Host Only Networking

 By default, docker deploys a host-only bridge adapter. Containers are able to communicate with one
 another if you forward host ports to the containers using the `-p` option. More on this in the
[Deploying Containers]({{site.url}}/user/deploying-containers.html) docpage.

 There are other ways to enable cross-host communication using
 [Supporting Charms](http://github.com/chuckbutler/flannel-docker-charm) that will enable an
 overlay-network - but are outside the scope of these help pages.

#### Offline Environments

There is no support for installation of the docker service in
[offline environments](https://jujucharms.com/docs/howto-offline-charms).
There is however [a bug](https://github.com/chuckbutler/docker-charm/issues/13) to track the
progress of this feature.

#### AUFS Upgrade Stopped my containers from working

If you have older containers deployed and running, you will need to pause them
and export. Once the tarballs of the containers have been exported - upgrade
your cluster and reimport following the CLI instructions below as a guide

    docker export <<container id>> > mycontainer-latest.tgz
    # upgrade
    docker import -i mycontainer-latest - mycontainer:latest
    docker run <<options>> mycontainer:latest


# Contact Information

- Author: Charles Butler &lt;[charles.butler@ubuntu.com](mailto:charles.butler@ubuntu.com)&gt;

## Docker Upstream

- [Docker website](http://docker.io)
- [Docker bug tracker](http://github.com/docker/docker/issues)
- [Docker users mailing list](https://groups.google.com/forum/?fromgroups#!forum/docker-users)
- [Docker dev mailing list](https://groups.google.com/forum/?fromgroups#!forum/docker-dev)
