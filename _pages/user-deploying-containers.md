---
layout: default
title: Deploying Containers
category: User Docs
permalink: /user/deploying-containers.html
---

# Juju Run Deployment

`juju run` is a great command to interface with docker on the remote host.

> **Warning!** `juju run` executes as different users in different contexts.
> You can validate this assertion by running `whoami` in the context.
> Therefore, we recommend you always scope the run to the specific unit you want
> to target. There is more on this in the
> [Working with units](https://jujucharms.com/docs/charms-working-with-units)
> docs.


All commands specifying a unit will assume the service is named `docker` and we are
scoping our command to the first unit in the service group. Substitute commands as
required.

The response from a `juju run` command may take a bit to return - as this is not an asynchronus
operation. The default timeout for running a command via `juju run` is five minutes. If there is
an operation that takes an exceptionally long time to run, it may be more prudent to run it in
an interactive terminal via [Juju SSH](#juju-ssh)

##### Pulling and running containers in the public registry

Depending on which service you are deploying - you can verify that you have connectivity
to the docker hub by pulling a small image and running it. The following will pull a tinyrss
feed reader and its dependent postgresql database, linking them together with docker and expose
the web interface for inspection.

    juju run --unit docker/0 "docker run -d --name ttrssdb nornagon/postgres"
    juju run --unit docker/0 "docker run -d --link ttrssdb:db -p 8000:80 clue/ttrss"

You can now verify the docker portmapping is working:

    juju run --unit docker/0 "curl localhost:8000

And you should see the raw HTML of our TinyRSS service


> **Note:** There is additional work required to expose the service to the world at large. Just
> browsing to the public-ip:port of the service at present is insufficient on AWS. Other providers
> have not been verified.


##### Verifying Running Containers

    juju run --unit docker/0 "docker ps"

output

    > CONTAINER ID        IMAGE                      COMMAND                CREATED             STATUS              PORTS                  NAMES
    > fa50d720d493        clue/ttrss:latest          /bin/sh -c 'php /con   3 minutes ago       Up 3 minutes        0.0.0.0:8000->80/tcp   furious_fermi              
    > 2770c248ce0a        nornagon/postgres:latest   /usr/lib/postgresql/   7 minutes ago       Up 7 minutes        5432/tcp               furious_fermi/db,ttrssdb 

# Juju SSH

Some commands may require interaction, such as logging into the docker registry, or interfacing
with your own private registry. This is where `juju ssh` will enable you to log into an interactive
shell on the remote host to perform such operations.

    juju ssh docker/0
    docker login
    > username: bobvilla
    > password: ********
    > email: bob@homeimprovement.com


