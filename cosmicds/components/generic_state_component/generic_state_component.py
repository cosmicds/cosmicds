from ipyvuetify import VuetifyTemplate
from traitlets import Unicode

from cosmicds.cds_glue_state import CDSGlueState
from cosmicds.utils import load_template

class GenericStateComponent(VuetifyTemplate):

    template = Unicode().tag(sync=True)
    state = CDSGlueState().tag(sync=True)

    def __init__(self, filename, path, state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = state
        self.template = load_template(filename, path)
