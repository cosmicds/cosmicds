from cosmicds.components.viewer_layout import ViewerLayout
from cosmicds.events import StepSetupMessage, StepChangeMessage
from cosmicds.registries import register_stage
from cosmicds.utils import load_template
from echo import CallbackProperty
from echo.containers import DictCallbackProperty
from glue.core import HubListener
from glue.core.state_objects import State
from glue_jupyter.state_traitlets_helpers import GlueState
from glue_wwt.viewer.jupyter_viewer import WWTJupyterViewer
from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from ipywidgets.widgets import widget
from traitlets import Dict, List, Unicode, Int
from glue_jupyter.bqplot.scatter import BqplotScatterView


class StageOneState(State):
    pass


@register_stage(story="hubbles_law", index=2, steps=[
    "Explore celestial sky",
    "Collect galaxy data",
    "Measure spectra",
    "Reflect",
    "Calculate velocities"
])
class StageOne(VuetifyTemplate, HubListener):
    template = load_template("stage_one.vue", __file__).tag(sync=True)
    state = GlueState().tag(sync=True)
    story_state = GlueState().tag(sync=True)
    title = Unicode("Do someting else").tag(sync=True)
    subtitle = Unicode("Perhaps a small blurb about this stage").tag(sync=True)
    viewers = Dict().tag(sync=True, **widget_serialization)

    def __init__(self, story_state, session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.story_state = story_state
        self._session = session
        self.state = StageOneState()
        
        return

        # Load the viewers for this stage
        wwt_viewer = self.app.new_data_viewer(
            BqplotScatterView, data=None, show=False)

        # data = self.data_collection['galaxy_data']
        # wwt_viewer.state.lon_att = data.id['RA_deg']
        # wwt_viewer.state.lat_att = data.id['Dec_deg']

        # Store an internal collection of the glue viewer objects
        self._viewer_handlers = {
            'wwt_viewer': wwt_viewer,
        }

        # Store a front-end accessible collection of renderable ipywidgets
        self.viewers = {k : ViewerLayout(v) for k, v in self._viewer_handlers.items()}
        
    @property
    def app(self):
        return self._session.application

    @property
    def session(self):
        return self._session
