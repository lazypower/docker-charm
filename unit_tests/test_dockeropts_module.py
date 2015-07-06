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
                 path="/wat/hey.yaml")


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


def test_simple_write_data(docker_opts, tempdir):
    amo = ansible_module_obj(dict(key='wat',
                                  val='hey',
                                  yaml=tempdir / "opts.yaml",
                                  action="set"))

    dom = docker_opts.DockerOptsManager(amo)
    out = dom.dispatch()
    assert amo.exit_json.called

    args = amo.exit_json.call_args[1]
    assert args
    assert args['msg'].startswith("Created key wat=hey in /tmp/docker_opts_test")
    assert args['changed']

    assert dom.path.exists()
    txt = dom.path.text()
    data = yaml.safe_load(txt)
    assert 'wat' in data and data['wat'] == 'hey'
