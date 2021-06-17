from echo import CallbackProperty, DictCallbackProperty, ListCallbackProperty
from glue.core.state_objects import State
from glue_jupyter.app import JupyterApplication
from glue_jupyter.bqplot import scatter
from glue_jupyter.state_traitlets_helpers import GlueState
from ipyvuetify import VuetifyTemplate
from .utils import load_template
from traitlets import Dict, Bool, List, Int
from glue_jupyter.bqplot.profile import BqplotProfileView
from glue_jupyter.bqplot.image import BqplotImageView
from ipywidgets import widget_serialization
import numpy as np
from glue_jupyter.vuetify_layout import vuetify_layout_factory



class ApplicationState(State):
    footer_link_items = ListCallbackProperty([
        'Home',
        'About Us',
        'Team',
        'Services',
        'Blog',
        'Contact Us',
    ])
    e1 = CallbackProperty(1)


class Application(VuetifyTemplate):
    _metadata = Dict({"mount_id": "content"}).tag(sync=True)
    state = GlueState().tag(sync=True)
    template = load_template("app.vue", __file__).tag(sync=True)
    viewers = Dict().tag(sync=True, **widget_serialization)
    items = List().tag(sync=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state = ApplicationState()
        self._application_handler = JupyterApplication()
        self._application_handler.load_data("/Users/nmearl/Downloads/w5/w5.fits")

        image_viewer = self._application_handler.imshow(show=False)
        image_viewer_layout = vuetify_layout_factory(image_viewer)

        scatter_viewer = self._application_handler.scatter2d(x='Right Ascension', y='Declination', show=False)
        scatter_viewer_layout = vuetify_layout_factory(scatter_viewer)

        self.viewers = {
            'image_viewer': image_viewer_layout, 
            'profile_viewer': scatter_viewer_layout
        }

    @property
    def session(self):
        return self._application_handler.session