from glue.core.state_objects import State
from ipywidgets import widget_serialization
from traitlets import Dict, List
from cosmicds.registries import story_registry
from echo import CallbackProperty

from .stages import StageOne, StageTwo


@story_registry(name="hubbles_law")
class HubbleStoryState(State):
    stages = CallbackProperty([])
