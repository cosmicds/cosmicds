from .story import *
from .stages import *
from .viewers import *
from .tools import *

import ipyvue

comp_dir = Path(__file__).parent / "components"

for comp_path in comp_dir.iterdir():
    if comp_path.is_file and comp_path.suffix == ".vue":
        ipyvue.register_component_from_string(
            name=comp_path.stem.replace('_', '-'),
            value=comp_path.read_text())
