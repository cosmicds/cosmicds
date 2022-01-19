from os import sync
from os.path import join
from pathlib import Path

from astropy.modeling import models, fitting
from echo import CallbackProperty, DictCallbackProperty, add_callback
from cosmicds.components.viewer_layout import ViewerLayout
# from echo.containers import DictCallbackProperty
from echo.core import add_callback
from glue.core.state_objects import State
from glue_jupyter.app import JupyterApplication
from glue_jupyter.bqplot.histogram import BqplotHistogramView
from glue_jupyter.bqplot.image import BqplotImageView
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.state_traitlets_helpers import GlueState
from glue_wwt.viewer.jupyter_viewer import WWTJupyterViewer
import ipyvuetify as v
from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from traitlets import Dict, List, Instance, Int, Bool, observe
from .registries import story_registry, stage_registry

from voila.configuration import VoilaConfiguration
from voila.app import Voila

from .utils import load_template
from .events import StepChangeMessage, StepSetupMessage

v.theme.dark = True


class Application(VuetifyTemplate):
    _metadata = Dict({"mount_id": "content"}).tag(sync=True)
    story_state = GlueState().tag(sync=True)
    template = load_template("app.vue", __file__).tag(sync=True)
    drawer = Bool(True).tag(sync=True)

    def __init__(self, story, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._application_handler = JupyterApplication()
        self.story_state = story_registry.setup_story(story, self.session)

    def _on_step_setup(self, msg):
        pass

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
