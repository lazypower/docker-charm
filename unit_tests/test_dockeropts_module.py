import yaml
from mock import Mock
from mock import call
from path import path
from unittest import TestCase
import pytest
import sys
import tempfile

# https://pytest.org/latest/fixture.html

here = path(__file__).parent

def read_data(manager):
    """
    Read the yaml from a file using the manager path return the data object.
    """
    assert manager.path.exists()
    txt = manager.path.text()
    data = yaml.safe_load(txt)
    return data


@pytest.fixture
def docker_opts():
    sys.path.insert(0, str(here.parent / "modules"))
    import docker_opts
    return docker_opts


@pytest.fixture
def paramed_object(docker_opts):

    class Classy(object):
        wat = docker_opts.param("wat", path)
        ok = docker_opts.param("ok")

        def __init__(self, **kw):
            self.mod = Mock(name="ansible-module")
            self.params = kw
    return Classy(wat="/etc", ok=True)


@pytest.fixture(scope="module")
def tempdir(request):
    tmpdir = path(tempfile.mkdtemp(prefix="docker_opts_test-"))
    request.addfinalizer(tmpdir.rmtree)
    return tmpdir


def_state = dict(key='wat',
                 val='yeah',
                 action='ok',
                 yaml="/wat/hey.yaml")


@pytest.fixture
def ansible_module_obj(state=def_state):
    amo = Mock(name="module")

    def getter(key):
        return state.get(key)

    amo.params.get.side_effect = getter
    return amo


def test_param(paramed_object):
    assert paramed_object.ok
    assert isinstance(paramed_object.wat, path)


def test_init(docker_opts, ansible_module_obj):

    dom = docker_opts.DockerOptsManager(ansible_module_obj)

    assert dom.action == 'ok'
    assert dom.val == 'yeah'


def test_add_remove(docker_opts, tempdir):
    """
    Verify the collection methods: add and remove work with test data.
    """
    key = 'add-remove-key'
    value = 'add-remove-value'
    filepath = tempdir / 'add_remove.yaml'
    amo = ansible_module_obj(dict(key=key,
                                  val=value,
                                  yaml=filepath,
                                  action='add'))
    dom = docker_opts.DockerOptsManager(amo)
    out = dom.dispatch()
    data = read_data(dom)

    # Verify the value is in the collection at data[key]
    assert key in data and value in data[key]
    # Now remove the key from the collection.
    amo = ansible_module_obj(dict(key=key,
                                  val=value,
                                  yaml=filepath,
                                  action='remove'))
    dom = docker_opts.DockerOptsManager(amo)
    out = dom.dispatch()
    data = read_data(dom)
    # Verify the value was removed from the collection.
    assert key in data and value not in data[key]


def test_set_delete(docker_opts, tempdir):
    """
    Verify the key/value methods: set and delete work with test data.
    """
    key = 'set-delete-key'
    value = 'set-delete-value'
    filepath = tempdir / 'set_delete.yaml'
    amo = ansible_module_obj(dict(key=key,
                                  val=value,
                                  yaml=filepath,
                                  action='set'))
    dom = docker_opts.DockerOptsManager(amo)
    out = dom.dispatch()
    data = read_data(dom)
    # Verify that the value is equal to the data[key]
    assert key in data and data[key] == value
    # Now delete the key from the data object.
    amo = ansible_module_obj(dict(key=key,
                                  val=value,
                                  yaml=filepath,
                                  action='delete'))
    dom = docker_opts.DockerOptsManager(amo)
    out = dom.dispatch()
    data = read_data(dom)
    # Verify the value was removed from the data object.
    assert key not in data


def test_read(docker_opts, tempdir):
    """
    Verify the read method works on the DockerOptsManager class.
    """
    key = 'read-key'
    value = 'read-value'
    filepath = tempdir / 'read.yaml'
    amo = ansible_module_obj(dict(key=key,
                                  val=value,
                                  yaml=filepath,
                                  action='read'))
    dom = docker_opts.DockerOptsManager(amo)
    # The data propery reads the file, which is non existant.
    dom.read(dom.data)
    assert dom.exit.called
    args = dom.exit.call_args[1]
    assert args
    # Ensure the docker_daemon_opts are empty.
    assert args['ansible_facts']['docker_daemon_opts'] == ''
    amo = ansible_module_obj(dict(key=key,
                                  val=value,
                                  yaml=filepath,
                                  action='set'))
    dom = docker_opts.DockerOptsManager(amo)
    dom.dispatch()
    # Now read the file, and it should have the key and value inside.
    dom.read(dom.data)
    assert dom.exit.called
    args = dom.exit.call_args[1]
    assert args
    options = '--{0} {1}'.format(key, value)
    # Ensure the docker_daemon_opts match the options string.
    assert args['ansible_facts']['docker_daemon_opts'] == options


def test_simple_set(docker_opts, tempdir):
    amo = ansible_module_obj(dict(key='wat',
                                  val='hey',
                                  yaml=tempdir / 'set.yaml',
                                  action='set'))
    dom = docker_opts.DockerOptsManager(amo)
    out = dom.dispatch()
    assert amo.exit_json.called

    args = amo.exit_json.call_args[1]
    assert args
    assert args['msg'].startswith("Created key wat=hey in /tmp/docker_opts_test")
    assert args['changed']

    data = read_data(dom)
    assert 'wat' in data and data['wat'] == 'hey'
