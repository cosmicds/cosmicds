import json
import os
from os import getenv

import ipyvuetify as v
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
from .utils import CDSJSONEncoder, debounce, load_template, request_session

v.theme.dark = True


class ApplicationState(State):
    using_voila = CallbackProperty(False)
    dark_mode = CallbackProperty(True)
    student = CallbackProperty({})
    classroom = CallbackProperty({})
    update_db = CallbackProperty(False)
    show_team_interface = CallbackProperty(True)
    allow_advancing = CallbackProperty(True)
    speech_pitch = CallbackProperty(1)
    speech_rate = CallbackProperty(1)
    speech_autoread = CallbackProperty(False)
    speech_voice = CallbackProperty(None)


class Application(VuetifyTemplate, HubListener):
    _metadata = Dict({"mount_id": "content"}).tag(sync=True)
    story_state = GlueState().tag(sync=True)
    template = load_template("app.vue", __file__, traitlet=True).tag(sync=True)
    drawer = Bool(True).tag(sync=True)
    speech_menu = Bool(False).tag(sync=True)
    vue_components = Dict().tag(sync=True, **widget_serialization)
    app_state = GlueState().tag(sync=True)
    student_id = Int(0).tag(sync=True)
    show_snackbar = Bool(False).tag(sync=True)
    hub_user_info = Dict().tag(sync=True)
    hub_user_loaded = Bool(False).tag(sync=True)

    def __init__(self, story, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app_state = ApplicationState()

        self.app_state.update_db = kwargs.get("update_db", True)
        self.app_state.show_team_interface = kwargs.get("show_team_interface",
                                                        True)

        self.app_state.allow_advancing = kwargs.get("allow_advancing", False)

        self.request_session = request_session()

        # NOTE: This procedure is only valid when using ContainDS
        if "JUPYTERHUB_USER" in os.environ:
            self.observe(lambda x: self._setup(story, **kwargs), 'hub_user_info')
        else:
            self._setup(story, **kwargs)

    def _setup(self, story, **kwargs):
        db_init = False

        create_new = kwargs.get("create_new_student", False)

        if create_new:
            response = self.request_session.get(f"{API_URL}/new-dummy-student").json()
            self.app_state.student = response["student"]
            self.app_state.classroom["id"] = 0
            self.student_id = self.app_state.student["id"]
            db_init = True
        else:
            username = self.hub_user_info.get('name', getenv("JUPYTERHUB_USER"))

            if username is not None:
                r = self.request_session.get(f"{API_URL}/student/{username}")
                student = r.json()["student"]
                if student is not None:
                    self.app_state.student = student
                    self.student_id = student["id"]

            if not self.app_state.student:
                sid = kwargs.get("student_id", 0)
                self.app_state.student["id"] = sid
                self.student_id = sid
            
        class_response = self.request_session.get(f"{API_URL}/class-for-student-story/{self.student_id}/{story}")
        class_json = class_response.json()
        cls = class_json["class"]
        size = class_json["size"]
        self.app_state.classroom = cls or { "id": 0 }
        self.app_state.classroom["size"] = size

        # print(f"Student ID: {self.student_id}")
        # print(f"Class ID: {self.app_state.classroom['id']}")

        self._application_handler = JupyterApplication()
        self.story_state = story_registry.setup_story(story, self.session, self.app_state)

        self._get_student_options()

        # Initialize from database
        if db_init:
            self._initialize_from_database()

        # Subscribe to events
        self.hub.subscribe(self, WriteToDatabaseMessage,
                           handler=self._on_write_to_database)

        add_callback(self.app_state, 'dark_mode', self._theme_toggle)
        add_callback(self.app_state, 'speech_rate', self._speech_rate_changed)
        add_callback(self.app_state, 'speech_pitch', self._speech_pitch_changed)
        add_callback(self.app_state, 'speech_autoread', self._speech_autoread_changed)
        add_callback(self.app_state, 'speech_voice', self._speech_voice_changed)

        self.hub_user_loaded = True
        self.show_snackbar = True

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

    @property
    def student_options_endpoint(self):
        user = self.app_state.student
        return f"{API_URL}/options/{user['id']}"

    def _initialize_from_database(self):
        try:
            # User information for a JupyterHub notebook session is stored in an
            # environment variable
            # user = os.environ['JUPYTERHUB_USER']
            response = self.request_session.get(self.story_state_endpoint)
            data = response.json()
            state = data["state"]
            if state is not None:
                self.story_state.update_from_dict(state)
        except Exception as e:
            print(e)

    def _get_student_options(self):
        # Get any persistent student options
        try:
            response = self.request_session.get(self.student_options_endpoint)
            data = response.json()
            if data is not None:
                data.pop("student_id", 0)
                self.app_state.update_from_dict(data)
        except ValueError as e:
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
            self.request_session.put(self.story_state_endpoint, json=data)

    def vue_write_to_database(self, _args=None):
        self._on_write_to_database(None)

    def vue_update_state(self, _args=None):
        trait = self.traits()["story_state"]
        trait.on_state_change(obj=self)

    def vue_update_mc_score(self, args):
        index = self.story_state.stage_index
        key = str(index)
        if key not in self.story_state.mc_scoring:
            self.story_state.mc_scoring[key] = {}

        self.story_state.mc_scoring[key][args["tag"]] = {
            "score": args["score"],
            "choice": args["choice"],
            "tries": args["tries"]
        }

    def vue_update_free_response(self, args):
        index = self.story_state.stage_index
        key = str(index)
        if key not in self.story_state.responses:
            self.story_state.responses[key] = {}
        self.story_state.responses[key][args["tag"]] = args["response"]

    def _theme_toggle(self, dark):
        v.theme.dark = dark

    def _student_option_changed(self, option, value):
        url = self.student_options_endpoint
        self.request_session.put(url, json={
            "option": option,
            "value": value
        })

    @debounce(1)
    def _speech_rate_changed(self, rate):
        self._student_option_changed('speech_rate', rate)

    @debounce(1)
    def _speech_pitch_changed(self, pitch):
        self._student_option_changed('speech_pitch', pitch)

    @debounce(1)
    def _speech_autoread_changed(self, autoread):
        self._student_option_changed('speech_autoread', autoread)

    @debounce(1)
    def _speech_voice_changed(self, voice):
        self._student_option_changed('speech_voice', voice)
