import json

import ipyvuetify as v
import requests
from cosmicds.utils import API_URL
from echo import add_callback, CallbackProperty
from glue.core import HubListener
from glue.core.state_objects import State
from glue_jupyter.app import JupyterApplication
from glue_jupyter.state_traitlets_helpers import GlueState
from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from traitlets import Dict, Bool, Int

from .events import WriteToDatabaseMessage
from .registries import story_registry
from .utils import CDSJSONEncoder, load_template

v.theme.dark = True


class ApplicationState(State):
    using_voila = CallbackProperty(False)
    dark_mode = CallbackProperty(True)
    student = CallbackProperty({})
    classroom = CallbackProperty({})
    update_db = CallbackProperty(False)
    show_team_interface = CallbackProperty(True)


class Application(VuetifyTemplate, HubListener):
    _metadata = Dict({"mount_id": "content"}).tag(sync=True)
    story_state = GlueState().tag(sync=True)
    template = load_template("app.vue", __file__, traitlet=True).tag(sync=True)
    drawer = Bool(True).tag(sync=True)
    vue_components = Dict().tag(sync=True, **widget_serialization)
    app_state = GlueState().tag(sync=True)
    student_id = Int(0).tag(sync=True)

    def __init__(self, story, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app_state = ApplicationState()

        self.app_state.update_db = kwargs.get("update_db", True)
        self.app_state.show_team_interface = kwargs.get("show_team_interface",
                                                        True)

        db_init = False
        create_new = kwargs.get("create_new_student", False)
        if create_new:
            response = requests.get(f"{API_URL}/new-dummy-student").json()
            self.app_state.student = response["student"]
            self.app_state.classroom["id"] = 0
            db_init = True
        else:
            self.app_state.classroom["id"] = kwargs.get("class_id", 0)
            self.app_state.student["id"] = kwargs.get("student_id", 0)
        self.student_id = self.app_state.student["id"]
        print(f"Student ID: {self.student_id}")

        self._application_handler = JupyterApplication()
        self.story_state = story_registry.setup_story(story, self.session,
                                                      self.app_state)

        # Initialize from database
        if db_init:
            self._initialize_from_database()
            pass

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

    @property
    def story_state_endpoint(self):
        user = self.app_state.student
        story = self.story_state.name
        return f"{API_URL}/story-state/{user['id']}/{story}"

    def _initialize_from_database(self):
        try:
            # User information for a JupyterHub notebook session is stored in an
            # environment variable
            # user = os.environ['JUPYTERHUB_USER']
            response = requests.get(self.story_state_endpoint)
            data = response.json()
            state = data["state"]
            if state is not None:
                self.story_state.update_from_dict(state)
        except Exception as e:
            print(e)

    def _on_write_to_database(self, _msg=None):
        if not self.app_state.update_db:
            return

        # User information for a JupyterHub notebook session is stored in an
        # environment variable
        # user = os.environ['JUPYTERHUB_USER']

        data = json.loads(
            json.dumps(self.story_state.as_dict(), cls=CDSJSONEncoder))
        if data:
            requests.put(self.story_state_endpoint, json=data)

    def vue_write_to_database(self, _args=None):
        self._on_write_to_database(None)

    def vue_update_state(self, _args=None):
        trait = self.traits()["story_state"]
        trait.on_state_change(obj=self)

    def vue_update_mc_score(self, args):
        index = self.story_state.stage_index
        if index not in self.story_state.mc_scoring:
            self.story_state.mc_scoring[index] = {}

        self.story_state.mc_scoring[index][args["tag"]] = {
            "score": args["score"],
            "choice": args["choice"],
            "tries": args["tries"]
        }

    def _theme_toggle(self, dark):
        v.theme.dark = dark
