import ipyvuetify as v
import pymongo
import os
from echo import CallbackProperty
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

v.theme.dark = True

# Setup database connections
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client['cosmicds']

class ApplicationState(State):
    using_voila = CallbackProperty(False)
    dark_mode = CallbackProperty(True)

class Application(VuetifyTemplate, HubListener):
    _metadata = Dict({"mount_id": "content"}).tag(sync=True)
    story_state = GlueState().tag(sync=True)
    template = load_template("app.vue", __file__, traitlet=True).tag(sync=True)
    drawer = Bool(False).tag(sync=True)
    vue_components = Dict().tag(sync=True, **widget_serialization)
    darkmode = Bool(True).tag(sync=True)
    app_state = ApplicationState()

    def __init__(self, story, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._application_handler = JupyterApplication()
        self.story_state = story_registry.setup_story(story, self.session, self.app_state)

        # Initialize from database
        self._initialize_from_database()

        # Subscribe to events
        self.hub.subscribe(self, WriteToDatabaseMessage,
                           handler=self._on_write_to_database)

        self.observe(self._theme_toggle, names=['darkmode'])

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
            user = os.environ['JUPYTERHUB_USER']
            stories = database[self.story_state.name]
            story_data = stories.find_one({
                'name': self.story_state.name,
                'student_user': user})

            # Update story state with retrieved database data
            if story_data is not None:
                self.story_state.update_from_dict(story_data)
        except:
            pass

    def _on_write_to_database(self, msg):
        # User information for a JupyterHub notebook session is stored in an
        # environment  variable
        user = os.environ['JUPYTERHUB_USER']

        # Connect to story's collection
        stories = database[self.story_state.name]
        story_data = self.story_state.as_dict()

        stories.update_one({'student_user': user}, story_data, upsert=True)

    def _theme_toggle(self, change):
        v.theme.dark = change["new"]