import ipyvuetify as v
from cosmicds.utils import load_template
from echo import add_callback
from glue_jupyter.state_traitlets_helpers import GlueState
from traitlets import Unicode

class DistanceSidebar(v.VuetifyTemplate):

    template = load_template("distance_sidebar.vue", __file__, traitlet=True).tag(sync=True)
    state = GlueState().tag(sync=True)
    angular_height = Unicode().tag(sync=True)
    angular_size = Unicode().tag(sync=True)

    galaxy_type = Unicode().tag(sync=True)
    height = Unicode().tag(sync=True)
    angular_size = Unicode().tag(sync=True)

    def __init__(self, state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = state
        add_callback(self.state, 'selected_galaxy', self._on_galaxy_update)

    def _on_galaxy_update(self, galaxy):
        self.galaxy_type = galaxy["Type"]

    def vue_add_distance_data_point(self):
        self.state.make_measurement = True
