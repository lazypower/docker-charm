#!/usr/bin/env python
from ansible.module_utils.basic import *  # noqa
import yaml
from path import path


class param(object):
    def __init__(self, key, type_=None):
        self.key = key
        self.type = type_

    def __get__(self, obj, type=None):
        val = obj.mod.params.get(self.key)
        if self.type is None:
            return val
        return self.type(val)


class DockerOptsManager(object):
    """
    Ansible module to manage a yaml file that holds key:val
    pairs representing docker options.

    Values may either be strings or sets.
    """
    action = param('action')
    key = param('key')
    val = param('val')
    path = param('yaml', path)

    def __init__(self, module):
        self.mod = module
        self.fail = module.fail_json
        self.exit = module.exit_json

    @staticmethod
    def make_module():
        # apparently only the * import modules
        # gets replacements
        module = AnsibleModule(
            argument_spec=dict(
                action=dict(default='read',
                            choices=['read',
                                     'set',
                                     'delete',
                                     'add',
                                     'remove']),
                yaml=dict(required=True, type='str'),
                key=dict(type='str'),
                val=dict(type='str'),
            )
        )
        return module

    @property
    def data(self):
        if self.path.exists():
            with open(self.path) as stream:
                data = yaml.safe_load(stream)
                return data
        return {}

    @staticmethod
    def multiops(sets):
        for key, coll in sets:
            for val in coll:
                yield "--{0} {1}".format(key, val)

    def read(self, data):
        di = data.items()
        flags = ["--%s %s" % (key, val)
                 for key, val in di
                 if isinstance(val, basestring)]

        sets = ((key, val) for key, val in di if isinstance(val, set))
        mops = list(self.multiops(sets))
        flags.extend(mops)
        docker_opts = " ".join(flags)

        return self.exit(changed=data and True or False,
                         msg="Data from %s" % self.path,
                         ansible_facts=dict(docker_daemon_opts=docker_opts))

    def write_data(self, data):
        new_yaml = yaml.safe_dump(data)
        self.path.write_text(new_yaml)

    def delete(self, data):
        changed = False
        if self.key in data:
            changed = True
            del data[self.key]
            self.write_data(data)
        return self.exit(changed=changed)

    def set(self, data):
        changed = False
        msg = "No change to %s" % self.path
        oldval = data.get(self.key, None)

        if isinstance(oldval, set):
            return self.fail("%s is a set" % self.key)

        newval = oldval != self.val
        if oldval is None or newval:
            changed = True
            data[self.key] = self.val
            action = newval and "Created" or "Updated"
            msg = "%s key %s=%s in %s" % (action,
                                          self.key,
                                          self.val,
                                          self.path)
            self.write_data(data)
        return self.exit(changed=changed, msg=msg)

    def add(self, data):
        changed = False
        msg = "No change to %s" % self.path
        oldset = data.setdefault(self.key, set())
        if not isinstance(oldset, set):
            return self.fail(msg="%s is not a set")

        if self.val not in oldset:
            changed = True
            msg = "Added %s to %s:%s" % (self.val, self.key, oldset)
            oldset.add(self.val)
            self.write_data(data)
        return self.exit(changed=changed, msg=msg)

    def remove(self, data):
        changed = False
        msg = "No change to %s" % self.path
        oldset = data.get(self.key, None)
        if oldset is not None or not isinstance(oldset, set):
            return self.fail(msg="%s is not a set")
        if self.val in oldset:
            changed = True
            msg = "Removed %s from %s:%s" % (self.val, self.key, oldset)
            oldset.remove(self.val)
            self.write_data(data)
        return self.exit(changed=changed, msg=msg)

    def dispatch(self, action=None):
        if action is None:
            action = self.action

        action = getattr(self, action, None)
        return action(self.data)

    @classmethod
    def main(cls):
        module = cls.make_module()
        om = cls(module)
        return om.dispatch()


if __name__ == '__main__':
    DockerOptsManager.main()
