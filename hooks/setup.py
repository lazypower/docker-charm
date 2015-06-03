import subprocess
import os
import sys


def pre_install():
    """
    Do any setup required before the install hook.
    """
    try:
        import ansiblecharm  # noqa
        from path import path  # noqa
    except ImportError:
        subprocess.check_call(['hooks/setup.sh'])
        subprocess.check_call("pip install -r hooks/python-pkgs.txt",
                              shell=True)
