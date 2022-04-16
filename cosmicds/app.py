import ipyvuetify as v
import requests
import os
from echo import add_callback, CallbackProperty
from glue.core.state_objects import State
from glue_jupyter.app import JupyterApplication
from glue_jupyter.state_traitlets_helpers import GlueState
from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from traitlets import Dict, Bool
from glue.core import HubListener

from .events import StepChangeMessage, WriteToDatabaseMessage
from .registries import story_registry
from .utils import load_template

from cosmicds.utils import API_URL

v.theme.dark = True

class ApplicationState(State):
    using_voila = CallbackProperty(False)
    dark_mode = CallbackProperty(True)
    student = CallbackProperty({})

class Application(VuetifyTemplate, HubListener):
    _metadata = Dict({"mount_id": "content"}).tag(sync=True)
    story_state = GlueState().tag(sync=True)
    template = load_template("app.vue", __file__, traitlet=True).tag(sync=True)
    drawer = Bool(False).tag(sync=True)
    vue_components = Dict().tag(sync=True, **widget_serialization)
    app_state = GlueState().tag(sync=True)

    def __init__(self, story, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app_state = ApplicationState()
        
        # For testing purposes, we create a new dummy student on each startup
        self.app_state.student = requests.get(f"{API_URL}/new-dummy-student").json()

        self._application_handler = JupyterApplication()
        self.story_state = story_registry.setup_story(story, self.session, self.app_state)

        # Initialize from database
        self._initialize_from_database()

        # Subscribe to events
        self.hub.subscribe(self, WriteToDatabaseMessage,
                           handler=self._on_write_to_database)

        add_callback(self.app_state, 'dark_mode', self._theme_toggle)

    def reload(self):
        """
        Reload only the UI elements of the application.
        """
        self.template = load_template("app.vue", __file__, traitlet=False)

    @property
    def session(self):
        """
        Underlying glue-jupyter application session instance.
        """
        return self._application_handler.session

    @property
    def data_collection(self):
        """
        Underlying glue-jupyter application data collection instance.
        """
        return self._application_handler.data_collection

    @property
    def hub(self):
        return self._application_handler.session.hub

    def _initialize_from_database(self):
        try:
            # User information for a JupyterHub notebook session is stored in an
            # environment  variable
            # user = os.environ['JUPYTERHUB_USER']
            user = self.app_state.student
            story = self.story_state.name
            self.story_state = requests.get(f"{API_URL}/story_state/{user.id}/{story}")
        except:
            pass

    def _on_write_to_database(self, msg):
        # User information for a JupyterHub notebook session is stored in an
        # environment  variable
        # user = os.environ['JUPYTERHUB_USER']

        user = self.app_state.student
        story = self.story_state.name
        requests.put(f"{API_URL}/story_state/{user.id}/{story}", data=self.story_state.as_dict())

    def _theme_toggle(self, dark):
        v.theme.dark = dark
