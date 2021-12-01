from cosmicds.registries import stage_registry
from cosmicds.utils import load_template
from glue.core import HubListener
from glue_jupyter.state_traitlets_helpers import GlueState
from ipyvuetify import VuetifyTemplate
from traitlets import Unicode


class StepperTwo(VuetifyTemplate, HubListener):
    template = load_template("stage_one.vue", __file__).tag(sync=True)
    state = GlueState().tag(sync=True)
    stage_title = Unicode("Collect Galaxy Data").tag(sync=True)
    stage_subtitle = Unicode("Something small to say").tag(sync=True)
    template = load_template("stepper_two.vue", __file__).tag(sync=True)

    def __init__(self, state, session, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state = state
        self._session = session


@stage_registry(name="hubbles_law", step=2)
class StageTwo(VuetifyTemplate, HubListener):
    template = load_template("stage_two.vue", __file__).tag(sync=True)
    state = GlueState().tag(sync=True)
    name = Unicode("Collect Galaxy Data").tag(sync=True)

    def __init__(self, state, session, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state = state
        self._session = session
        self.stepper = StepperTwo(self.state, self._session)

