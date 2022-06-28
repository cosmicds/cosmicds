# Licensed under a 3-clause BSD style license - see LICENSE.rst

from .version import __version__
__all__ = []

# Register any custom Vue components
from pathlib import Path
import ipyvue

comp_dir = Path(__file__).parent / "components"

for comp_path in comp_dir.iterdir():
    if comp_path.is_file and comp_path.suffix == ".vue":
        ipyvue.register_component_from_string(
            name=comp_path.stem.replace('_', '-'),
            value=comp_path.read_text())

from .stories import *
from .tools import *
