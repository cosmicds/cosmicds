# Licensed under a 3-clause BSD style license - see LICENSE.rst

from .version import __version__
import sys
import logging

__all__ = []

log = logging.getLogger()

# Register any custom Vue components
from pathlib import Path
import ipyvue

comp_dir = Path(__file__).parent / "components"

for comp_path in comp_dir.iterdir():
    if comp_path.is_file and comp_path.suffix == ".vue":
        ipyvue.register_component_from_string(
            name=comp_path.stem.replace('_', '-'),
            value=comp_path.read_text())

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

discovered_plugins = entry_points(group='cosmicds.plugins')

STORY_PATHS = {}

for ep in discovered_plugins:
    ep.load()
    log.info("Discovered the `%s` data story.", ep.name)

from .tools import *
