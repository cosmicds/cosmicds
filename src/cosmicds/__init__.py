import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


from pathlib import Path
import ipyvue
import re

from glue.config import settings

# Register any custom Vue components
comp_dir = Path(__file__).parent / "vue_components"


def load_custom_vue_components():
    for comp_path in comp_dir.rglob("*.vue"):
        if comp_path.is_file:
            comp_name = re.sub(r"(?<!^)(?=[A-Z])", "-", comp_path.stem).lower()
            ipyvue.register_component_from_file(
                name=comp_name,
                file_name=comp_path,
            )


# Override glue settings
settings.BACKGROUND_COLOR = "white"
settings.FOREGROUND_COLOR = "black"
