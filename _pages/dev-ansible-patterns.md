---
layout: default
title: Ansible Patterns
category: Developer Docs
permalink: /dev/ansible-patterns.html
---

### This guide is intended to help developers understand the considerations and patterns of the charm

We've made heavy use of ansible in the Docker Charm so approachability is fairly straight forward to anyone looking to contribute. You don't have to have an experience in any given programming language. If you can read YAML - and have a reference of the modules - you can write an Ansible Play.

To get started, there is a specific core set of things to understand about how the charm is put together.

### Charm Organization

There are 2 major directories - and 1 minor directory responsible for holding logic for the Docker Charm.

1. `hooks` - Contains the core suite of functional code to call ansible, and handle any meta tasks like installing ansible, and keeping ansible up to date.
2. `playbooks` - Contains the YAML files or *plays* that make up the configuration management of the charm.
3. `scripts` - warehouses 1-off scripts that didnt fit well in `hooks` or `playbooks`. Typically these are going to be in python, and are complimentary to the plays.

### The Call Stack / Operational Procedure

The core suite of hooks and hook logic is in `hooks/hooks.py`. This python file is responsible for calling out to the main playbook `site.yaml` and executing any plays that are tagged with the hook name.

For example, if the charm is in the `config-changed` hook. The order of execution is as follows:

1. Charm calls `hooks/config-changed`
2. `config-changed` is a symlink to hooks.py
3. `hooks.py` has a list of 'allowed hooks' in it, to ensure we have triaged adding new hooks in a methodical fashion.
4. `hooks.py` executes `ansible site.yaml`
5. Ansible scans the `site.yaml` file for plays tagged with `config-changed`
6. Execution of any plays happens and the hook exits 0

### A note about code quality / standards of playbooks

We have a make target for any developer looking to contribute to ensure we are using ansible best practices in our syntax. To ensure your code doesn't violate these coding standards, make sure you run the lint target associated with the project

    make lint

You will see any asssociated problems found along with the playbook that it encountered the problem. If you receive no output - everything is good to go!

##### A note about Unit Testing and Ansible

> Ansible is about infrastructure and having test for your playbooks themselves doesn’t really address if the infrastructure works. You can write a perfectly good playbook that doesn’t actually address any failings in the infrastructure.

This has been a controversial topic in the Ansible mailing list for a while. To read more about it, you can follow [this thread](https://groups.google.com/forum/#!topic/ansible-project/7VhqDDtf6Js) on their mailing list.

## Playbook and Play Shakedown

When you are adding a new connection to the docker charm - There are some patterns we already have in-place that will ensure your following the same practices we took while developing the charm.

1. Playbook names should be descriptive of the executing hook
2. Plays should be `- name:`'d with a description of what the play is doing.
3. Logic should be kept in the same playbook when it makes sense.
4. Massive logic files should be split apart based on logic path and concern


### When you have multiple paths of logic

Its fairly common to find 2 paths of logic within a playbook. To help isolate the playbooks to concerns and keep them very readable - if you have more than 5 plays in a single playbook that are guarded with a `when` statement, its feesable to break it apart into its own logical playbook and guard including that playbook with a `when` statement. If its fewer than 5 - think if it's really worth breaking apart into yet another file.

A ready example would be the logic branching depending on where Docker is coming from - if its the ubuntu universe archive package `docker.io`, or the upstream `lxc-docker` package. As this changes some environment settings (file naming, docker versions, behavior of the underlying service between these packages) And you can view the split in these three files:

- [playbooks/config-changed.yaml](https://github.com/chuckbutler/docker-charm/blob/master/playbooks/config-changed.yaml)
- [playbooks/latest-docker.yaml](https://github.com/chuckbutler/docker-charm/blob/master/playbooks/latest-docker.yaml)
- [playbooks/universe-docker.yaml](https://github.com/chuckbutler/docker-charm/blob/master/playbooks/universe-docker.yaml)

> We'll leave these decisions up to the developers - but may have commentary during Code Review on any pull requests.

### Pitfalls

The following issues have cropped up repeatedly during our ventures in developing this charm, and will serve as a knowledge base for developers looking to get started and how they can avoid the same papercuts we encountered.

- **Boolean operations** can be tricky in ansible- and may require some additional functional testing to ensure Ansible is casting the variable as you would expect it to be casting it.


