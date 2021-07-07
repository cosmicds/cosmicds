#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import os
import sys

from setuptools import setup
from setuptools.command.develop import develop


VERSION_TEMPLATE = """
# Note that we need to fall back to the hard-coded version if either
# setuptools_scm can't be imported or setuptools_scm can't determine the
# version, so we catch the generic 'Exception'.
try:
    from setuptools_scm import get_version
    __version__ = get_version(root='..', relative_to=__file__)
except Exception:
    __version__ = '{version}'
""".lstrip()


# These are based on jupyter_core.paths
def jupyter_config_dir():
    """Get the Jupyter config directory for this platform and user.
    Returns JUPYTER_CONFIG_DIR if defined, else ~/.jupyter
    """
    import pathlib
    from tempfile import mkdtemp

    env = os.environ
    home_dir = pathlib.Path.home().as_posix()

    if env.get('JUPYTER_NO_CONFIG'):
        return mkdtemp(suffix='jupyter-clean-cfg')

    if env.get('JUPYTER_CONFIG_DIR'):
        return env['JUPYTER_CONFIG_DIR']

    return os.path.join(home_dir, '.jupyter')


def user_dir():
    homedir = os.path.expanduser('~')
    # Next line will make things work even when /home/ is a symlink to
    # /usr/home as it is on FreeBSD, for example
    homedir = os.path.realpath(homedir)
    if sys.platform == 'darwin':
        return os.path.join(homedir, 'Library', 'Jupyter')
    elif os.name == 'nt':
        appdata = os.environ.get('APPDATA', None)
        if appdata:
            return os.path.join(appdata, 'jupyter')
        else:
            return os.path.join(jupyter_config_dir(), 'data')
    else:
        # Linux, non-OS X Unix, AIX, etc.
        import pathlib
        env = os.environ
        home = pathlib.Path.home().as_posix()
        xdg = env.get("XDG_DATA_HOME", None)
        if not xdg:
            xdg = os.path.join(home, '.local', 'share')
        return os.path.join(xdg, 'jupyter')


class DevelopCmd(develop):
    prefix_targets = [
        ("nbconvert/templates", 'cosmicds-default'),
        ("voila/templates", 'cosmicds-default')
    ]

    def run(self):
        target_dir = os.path.join(sys.prefix, 'share', 'jupyter')
        if '--user' in sys.prefix:  # TODO: is there a better way to find out?
            target_dir = user_dir()
        target_dir = os.path.join(target_dir)

        for prefix_target, name in self.prefix_targets:
            source = os.path.join('share', 'jupyter', prefix_target, name)
            target = os.path.join(target_dir, prefix_target, name)
            target_subdir = os.path.dirname(target)
            if not os.path.exists(target_subdir):
                os.makedirs(target_subdir)
            rel_source = os.path.relpath(os.path.abspath(
                source), os.path.abspath(target_subdir))
            try:
                os.remove(target)
            except Exception:
                pass
            print(rel_source, '->', target)
            os.symlink(rel_source, target)

        super(DevelopCmd, self).run()


# WARNING: all files generated during setup.py will not end up in the source
# distribution
data_files = []

# Add all the templates
for (dirpath, dirnames, filenames) in os.walk('share/jupyter/'):
    if filenames:
        data_files.append((dirpath, [os.path.join(dirpath, filename)
                                     for filename in filenames]))


setup(data_files=data_files, cmdclass={'develop': DevelopCmd},
      use_scm_version={'write_to': os.path.join('cosmicds', 'version.py'),
                       'write_to_template': VERSION_TEMPLATE})
