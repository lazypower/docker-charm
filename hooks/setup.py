import subprocess


def pre_install():
    """
    Do any setup required before the install hook.
    """
    try:
        import charmhelpers # noqa
        import ansiblecharm # noqa
        from path import path # noqa
    except ImportError:
        subprocess.check_call(['hooks/setup.sh'])
    from ansiblecharm.helpers import write_hosts_file
    write_hosts_file()
