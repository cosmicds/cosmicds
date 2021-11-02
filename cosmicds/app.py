from os.path import join
from pathlib import Path

from astropy.modeling import models, fitting
from echo import CallbackProperty
from echo.core import add_callback
from glue.core.state_objects import State
from glue_jupyter.app import JupyterApplication
from glue_jupyter.bqplot.histogram import BqplotHistogramView
from glue_jupyter.bqplot.image import BqplotImageView
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.state_traitlets_helpers import GlueState
from glue_wwt.viewer.jupyter_viewer import WWTJupyterViewer
from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from traitlets import Dict, List
from .registries import stage_registry

from .utils import load_template


class ApplicationState(State):
    drawer = CallbackProperty(True)
    step = CallbackProperty(0)


class Application(VuetifyTemplate):
    _metadata = Dict({"mount_id": "content"}).tag(sync=True)
    state = GlueState().tag(sync=True)
    template = load_template("app.vue", __file__).tag(sync=True)
    stages = Dict().tag(sync=True, **widget_serialization)

    def __init__(self, story, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state = ApplicationState()
        self._application_handler = JupyterApplication()

        if story not in stage_registry.members:
            raise ValueError(f"No story '{story}' found in registry. Available"
                " stories include:" + "\n\t".join(stage_registry.members))

        self.stages = {f"c-stage-{k}": v(self.session)
                       for k, v in dict(sorted(stage_registry.members[story].items())).items()}

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
