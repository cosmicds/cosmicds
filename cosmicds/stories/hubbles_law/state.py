
from typing import Dict
from glue.core.state_objects import State
from echo.containers import DictCallbackProperty, CallbackProperty
from cosmicds.registries import story_registry


@story_registry(name="hubbles_law")
class StoryState(State):
    stage_index = CallbackProperty(0)
    step_index = CallbackProperty(0)
    stages = DictCallbackProperty()