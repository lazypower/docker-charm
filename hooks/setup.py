import subprocess
import sys
import os


def pre_install():
    """
    Do any setup required before the install hook.
    """
    try:
        import charmhelpers #noqa
        import ansiblecharm  # noqa
        from path import path  # noqa
    except ImportError:
        subprocess.check_call(['hooks/setup.sh'])
        subprocess.check_call("pip install -r hooks/python-pkgs.txt",
                              shell=True)

        from path import path

        pth = str(path(os.environ['CHARM_DIR']) / 'src/ansiblecharm')
        sys.path.append(pth)
