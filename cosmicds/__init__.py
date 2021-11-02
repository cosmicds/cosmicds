# Licensed under a 3-clause BSD style license - see LICENSE.rst

from .version import __version__
__all__ = []

# Register any custom Vue components
from pathlib import Path
import ipyvue

vue_comp_dir = Path(__file__).parent / "data" / "vue_components"

for comp_path in vue_comp_dir.iterdir():
    if comp_path.suffix == ".vue":
        ipyvue.register_component_from_string(
            name=comp_path.stem.replace('_', '-'),
            value=comp_path.read_text())

from .stories.hubbles_law import *
