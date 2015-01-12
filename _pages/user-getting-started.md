---
layout: default
title: Getting Started
category: User Docs
permalink: /user/getting-started.html
---

# Deploying The Stable Charm

> The docker charm is not presently in the charm store.
> These instructions being applicable are pending a full charm review and acceptance to
> the charm-store. This warning will be removed upon promulgation of the charm.

    juju deploy cs:trusty/docker

The Deployment process will vary in time from provider to provider. Once the Docker charm
has been fully deployed it list an agent state of 'started' in the `juju status` output.

    services:
      docker:
        charm: cs:trusty/docker-0
        exposed: false
        units:
          ubuntu/0:
            agent-state: started
            agent-version: 1.21-beta4.1
            machine: "1"
            public-address: 172.31.2.54

You can remote into the docker unit and begin deploying containers immediately following the
[Post installation instructions](#post-installation-instructions).

# Deploying The Development Charm

> **Warning:** Deploying the Development Focus is not guaranteed to be stable - and not recommended
> for production deployments!

The Docker charm will be in varying states in the master branch of it's github repository. We
attempt to follow [Semantic Versioning](http://semver.org/) as closely as we can - to tag the
snapshots of the charm in specifics states of evolution. *This will not resemble the versioning
in the juju charm store*.

    mkdir -p ~/charms/trusty
    export JUJU_REPOSITORY=$HOME/charms
    git clone https://github.com/chuckbutler/docker-charm.git ~/charms/trusty/docker
    juju deploy local:trusty/docker

You can remote into the docker unit and begin deploying containers immediately following the
[Post installation instructions](#post-installation-instructions).

# Unit Constraints

The docker charm is very light weight and has been tested on several providers smallest units
without any issue. The performance of the overall stack will vary depending on the workload, and
you are encouraged to view the [Using Constraints](https://jujucharms.com/docs/charms-constraints)
 documentation.

- AWS m3.small
- HPCloud Standard Extra Small
- Azure A0 Tier
- Digital Ocean 512mb droplets


# Post Installation Instructions

Once the charm has been deployed - you can start to interface with docker right away.

The Ubuntu user has direct access to the `docker` command, and can be used for any of
the docker administrative tasks, such as viewing running processes or even running
new containers, and doing image management. More on this in the
[Deploying Containers]({{ site.url}}/user/deploying-containers.html) Documentation.

You may do this via `juju run` or via `juju ssh docker/0`. You can learn more about these
commands on the [working with units](https://jujucharms.com/docs/charms-working-with-units)
docpage on jujucharms.com.

# Known Limitations

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
