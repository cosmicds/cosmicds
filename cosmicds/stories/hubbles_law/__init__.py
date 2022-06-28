from .state import *
from .stages import *
from .viewers import *
from .tools import *

import ipyvue

vue_comp_dir = Path(__file__).parent / "components"

for comp_path in vue_comp_dir.iterdir():
    if comp_path.is_file and comp_path.suffix == ".vue":
        ipyvue.register_component_from_string(
            name=comp_path.stem.replace('_', '-'),
            value=comp_path.read_text())
