from echo import CallbackProperty, DictCallbackProperty, ListCallbackProperty
from glue.core.state_objects import State
from glue_jupyter.app import JupyterApplication
from glue_jupyter.state_traitlets_helpers import GlueState
from ipyvuetify import VuetifyTemplate


class ApplicationState(State):
    pass


class Application(VuetifyTemplate, JupyterApplication):
    _metadata = Dict({"mount_id": "content"}).tag(sync=True)
    state = GlueState().tag(sync=True)
    template = load_template("app.vue", __file__).tag(sync=True)
    
    def __init__(self, configuration=None, *args, **kwargs):
        super().__init__(*args, **kwargs)