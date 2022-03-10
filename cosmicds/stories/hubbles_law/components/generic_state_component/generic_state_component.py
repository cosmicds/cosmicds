from glue_jupyter.state_traitlets_helpers import GlueState
from ipyvuetify import VuetifyTemplate
from traitlets import Unicode

from cosmicds.utils import load_template

class GenericStateComponent(VuetifyTemplate):

    template = Unicode().tag(sync=True)
    state = GlueState().tag(sync=True)

    def __init__(self, name, state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = state
        self.template = load_template(f"{name}.vue", __file__)
