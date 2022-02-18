import logging

from glue.core.state_objects import State
from traitlets import default

from cosmicds.phases import Stage
from cosmicds.registries import register_stage
from cosmicds.utils import load_template

log = logging.getLogger()


class StageState(State):
    pass


@register_stage(story="hubbles_law", index=1, steps=[
    "Explore celestial sky",
    "Collect galaxy data",
    "Measure spectra",
    "Reflect",
    "Calculate velocities"
])
class StageTwo(Stage):
    @default('stage_state')
    def _default_state(self):
        return StageState()

    @default('template')
    def _default_template(self):
        return load_template("stage_one.vue", __file__)

    @default('title')
    def _default_title(self):
        return "Another Stage Name"

    @default('subtitle')
    def _default_subtitle(self):
        return "Perhaps a small blurb about this stage"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
