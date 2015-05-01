import subprocess


def pre_install():
    """
    Do any setup required before the install hook.
    """
    install_charmhelpers()


def install_charmhelpers():
    """
    Install the charmhelpers library, if not present.
    """
    try:
        import charmhelpers # noqa
        import ansible # noqa
        from path import path # noqa

    except ImportError:
        subprocess.check_call(['apt-get', 'install', '-y', 'python-pip'])
        subprocess.check_call(['apt-get', 'install', '-y', 'python-dev'])
        subprocess.check_call(['pip', 'install', '-e', 'git+https://github.com/whitmo/charmhelpers.git#egg=charmhelpers'])
        subprocess.check_call(['pip', 'install', 'ansible'])
        subprocess.check_call(['pip', 'install', 'path.py'])

    path('/etc/ansible/hosts').write_text('localhost')
