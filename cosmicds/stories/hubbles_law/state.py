
from typing import Dict
from glue.core.state_objects import State
from echo.containers import DictCallbackProperty, CallbackProperty
from cosmicds.registries import story_registry
from cosmicds.events import LoadDataMessage
from glue.core import Hub, HubListener
from pathlib import Path


@story_registry(name="hubbles_law")
class StoryState(State, HubListener):
    stage_index = CallbackProperty(0)
    step_index = CallbackProperty(0)
    stages = DictCallbackProperty()

    def __init__(self, session):
        super().__init__()

        self._session = session

        # Load data needed for Hubble's Law
        self.app.load_data(Path(__file__) / "data" / "hubbles_law_data.csv")

    @property
    def app(self):
        return self._session.application
