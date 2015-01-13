---
layout: default
title: Contributing to the Docker Charm
category: Developer Docs
permalink: /dev/contributing.html
---

Contributions are welcome, in any form. Whether that be Bugs, BugFixes, Documentation, or Features.

### Submitting a bug

1. Go to our [issue tracker](http://github.com/chuckbutler/docker-charm/issues) on GitHub
2. Search for existing issues using the search field at the top of the page
3. File a new issue including the info listed below
4. Thanks a ton for helping make the Docker Charm higher quality!

##### When filing a new bug, please include:

- **Descriptive title** - use keywords so others can find your bug (avoiding duplicates)
- **Steps to trigger the problem** - that are specific, and repeatable
- **What happens** - when you follow the steps, and what you expected to happen instead.
- Include the exact text of any error messages if applicable (or upload screenshots).
- Docker Charm version (or if you're pulling directly from Git, your current commit SHA - use git rev-parse HEAD) and the Juju Version output from `juju --version`.
- Did this work in a previous charm version? If so, also provide the version that it worked in.
- Any errors logged in `juju debug log` Console view

### Can I help fix a bug?

Yes please! But first...

- Make sure no one else is already working on it -- if the bug has a milestone assigned or is tagged 'fix in progress', then it's already under way. Otherwise, post a comment on the bug to let others know you're starting to work on it.

We use the Fork &amp; Pull model for distributed development. For a more in-depth overview: consult with the github documentation on [Collaborative Development Models](https://help.github.com/articles/using-pull-requests/#before-you-begin).

> ##### Fork & pull
>
> The fork & pull model lets anyone fork an existing repository and push changes to their personal fork without requiring access be granted to the source repository. The changes must then be pulled into the source repository by the project maintainer. This model reduces the amount of friction for new contributors and is popular with open source projects because it allows people to work independently without upfront coordination.

### Submitting a Bug Fix

The following checklist will help developers not familiar with the fork and pull process of development. We appreciate your enthusiasm to make the Docker Charm a High Quality experience! To Rapidly get started - follow the 8 steps below.

1. [Fork the repository](https://help.github.com/articles/fork-a-repo/)
2. Clone your fork `git clone git@github.com/myusername/docker-charm.git`
3. Checkout your topic branch with `git checkout -b my-awesome-bugfix`
4. Hack away at your feature/bugfix
5. Validate your bugfix if possible in the amulet test(s) so we dont reintroduce it later.
6. Commit code `git commit -a -m 'i did all this work to fix #32'`
7. Push your branch to your forks remote branch `git push origin my-awesome-bugfix`
8. Create the [Pull Request](https://help.github.com/articles/using-pull-requests/#initiating-the-pull-request)
9. Await Code Review
10. Rejoyce when Pull Request is accepted

### Submitting a Feature

The Steps are the same as [Submitting a Bug Fix](#submitting-a-bug-fix). If you want extra credit, make sure you [File an issue](http://github.com/chuckbutler/docker-charm/issues) that covers the Feature you are working on - as kind of a courtesy heads up. And assign the issue to yourself so we know you are working on it.

### Creating Documentation Fixes

We actually keep the docs in the same repository as the charm code, in a separate branch of `gh-pages`. This allows us to focus on the content of the documentation and they can be built/published in a lock-step version of the charm itself, and ensures that your contributions can be accepted quickly and efficiently published by simply merging a Pull Request.

### Submitting Documentation

The documentation is a static site generated from markdown in the `gh-pages` repository. With this in mind, we can version large swaths of documentation by simply changing permalinks, and then updating the navigation index. This allows us to be agile with our documentation, and keep it fresh and up to date without much hassle. 


1. [Fork the repository](https://help.github.com/articles/fork-a-repo/)
2. Clone your fork `git clone git@github.com/myusername/docker-charm.git`
3. Checkout the docs topic branch `git checkout gh-pages`
4. checkout a branch from the docs topic branch that is descriptive of your work `git checkout -b french-localization`
5. Hack away at your feature/bugfix
6. Commit code `git commit -a -m 'I translated the getting started page to french'`
7. Push your branch to your forks remote branch `git push origin french-localization`
8. Create the [Pull Request](https://help.github.com/articles/using-pull-requests/#initiating-the-pull-request) and target the `gh-pages` branch
9. Await Peer Review
10. Rejoyce when Pull Request is accepted



##### A note about documentation pages

Each doc page has what's called `front loaded metadata` that determines where the page lives, and how to build it. You can review an existing page for the metadata format.

    ---
    layout: default
    title: Contributing to the Docker Charm
    category: Developer Docs
    permalink: /dev/contributing.html
    ---
    body of page content starts here.

Ensuring your submitted pages have this metadata included will further expedite your merge proposal and ensure we keep things tidy on the site. Additionally we have a format for adjusting the sidebar navigation.

##### Navigation

Each section of the documentation is generated from data stored/warehoused in yaml files, and look like so:

    - title: Contributing
      url: dev/contributing.html

    - title: Ansible Patterns
      url: dev/ansible-patterns.html

These yaml arrays are parsed to build the navigation. If you add a topic page, ensure you've added it to the navigation. If you are submitting a Locale translation - we will need to adjust the core template to support your language - and appreciate your efforts and will get it included as quickly as possible. Thanks in advance for your patience!

