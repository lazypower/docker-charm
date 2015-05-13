import subprocess
import os
import sys


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
        subprocess.check_call("pip install -r hooks/python-pkgs.txt",
                              shell=True)

        from path import path

        #temporary dev hack
        for lib in ('src/ansiblecharm', 'src/charmhelpers'):
            pth = str(path(os.environ['CHARM_DIR']) / lib)
            sys.path.append(pth)

        from ansiblecharm import helpers
        helpers.write_hosts_file()
