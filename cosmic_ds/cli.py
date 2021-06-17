import logging
import pathlib
import os
import sys
import tempfile

import click
from voila.app import Voila
from voila.configuration import VoilaConfiguration

from cosmic_ds import __version__

CONFIGS_DIR = os.path.join(os.path.dirname(__file__), 'configs')


@click.version_option(__version__)
@click.command()
@click.argument('data-story', nargs=1, type=click.Path(exists=True))
def main(data_story):
    """
    Start a CosmicDS interactive instance from notebook provided by the
    ``data_story`` path.

    Parameters
    ----------
    filename : str
        The path to the data story to be loaded.
    """
    # Tornado Webserver py3.8 compatibility hotfix for windows
    if sys.platform == 'win32':
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    filepath = pathlib.Path(data_story).absolute()
    start_dir = os.path.abspath('.')

    try:
        logging.getLogger('tornado.access').disabled = True
        Voila.notebook_path = filepath
        VoilaConfiguration.template = 'cosmic-ds-default'
        VoilaConfiguration.enable_nbextensions = True
        VoilaConfiguration.file_whitelist = ['.*']
        sys.exit(Voila().launch_instance(argv=[]))
    finally:
        os.chdir(start_dir)


if __name__ == '__main__':
    main()