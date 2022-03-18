from .state import *
from .stages import *

import ipyvue

vue_comp_dir = Path(__file__).parent / "vue_components"

for comp_path in vue_comp_dir.iterdir():
    if comp_path.suffix == ".vue":
        ipyvue.register_component_from_string(
            name=comp_path.stem.replace('_', '-'),
            value=comp_path.read_text())
