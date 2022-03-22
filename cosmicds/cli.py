import logging
import os
import sys
import tempfile
from pathlib import Path

import click
from voila.app import Voila
from voila.configuration import VoilaConfiguration

from cosmicds import __version__

CONFIGS_DIR = os.path.join(os.path.dirname(__file__), 'configs')

STORY_PATHS = {
    'hubble': Path(__file__).parent.parent / "notebooks" / "CosmicDS.ipynb"
}


@click.version_option(__version__)
@click.command()
@click.argument('data_story', nargs=1)
def main(data_story):
    """
    Start a CosmicDS interactive instance from notebook provided by the
    ``data_story`` path.

    Parameters
    ----------
    data_story : str
        The dictionary key id referencing the notebook path.
    """

    # Tornado Webserver py3.8 compatibility hotfix for windows
    if sys.platform == 'win32':
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    filepath = STORY_PATHS.get(data_story, '.')
    start_dir = os.path.abspath('.')

    try:
        logging.getLogger('tornado.access').disabled = True
        Voila.notebook_path = filepath
        # Voila.tornado_settings = {'headers':{'Content-Security-Policy': 'frame-ancestors self *'}}
        VoilaConfiguration.template = 'cosmicds-default'
        VoilaConfiguration.enable_nbextensions = True
        VoilaConfiguration.file_whitelist = ['.*']
        VoilaConfiguration.show_tracebacks = True
        # VoilaConfiguration.connection_dir_root = jupyter_runtime_dir()
        VoilaConfiguration.preheat_kernel = True
        sys.exit(Voila().launch_instance(argv=[]))
    finally:
        os.chdir(start_dir)


if __name__ == '__main__':
    main()