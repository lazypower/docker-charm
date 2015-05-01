#!/usr/bin/env python
from charmhelpers.contrib.ansible import AnsibleHooks
from charmhelpers.contrib.ansible import install_ansible_support
import sys
import os

hook_names = [
    'install',
    'config-changed',
    'start',
    'stop',
    'upgrade-charm',
    'network-relation-changed',
    ]

hooks = AnsibleHooks(playbook_path='playbooks/site.yaml',
                     default_hooks=hook_names)


# @hooks.hook('install', 'upgrade-charm')
# def install():
#     """
#     Install or upgrade ansible.
#     """
#     install_ansible_support(from_ppa=True)



if __name__ == "__main__":
    hooks.execute(sys.argv, modules="%s/modules" % os.environ['CHARM_DIR'])
