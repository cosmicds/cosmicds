from pathlib import Path
from uuid import uuid4

import numpy as np
from echo import CallbackProperty, DictCallbackProperty, ListCallbackProperty
from echo.containers import CallbackList
from glue.core import Data
from glue.core.state_objects import State
from glue_jupyter.app import JupyterApplication
from glue_jupyter.bqplot.image import BqplotImageView
from glue_jupyter.bqplot.profile import BqplotProfileView
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.state_traitlets_helpers import GlueState
from glue_jupyter.vuetify_layout import vuetify_layout_factory
from glue_wwt.viewer.jupyter_viewer import WWTJupyterViewer
from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from traitlets import Bool, Dict, Int, List

from .utils import load_template
from .components.footer import Footer


class ApplicationState(State):
    over_model = CallbackProperty(1)
    col_tab_model = CallbackProperty(0)
    est_model = CallbackProperty(0)


class Application(VuetifyTemplate):
    _metadata = Dict({"mount_id": "content"}).tag(sync=True)
    state = GlueState().tag(sync=True)
    template = load_template("app.vue", __file__).tag(sync=True)
    viewers = Dict().tag(sync=True, **widget_serialization)
    items = List().tag(sync=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the vue components through the ipyvuetify machinery. We add the
        # html tag we want and an instance of the component class as a 
        # key-value pair to the components dictionary.
        self.components = {'c-footer': Footer(self)}

        self.state = ApplicationState()
        self._application_handler = JupyterApplication()
        
        # Load the galaxy position data
        self._application_handler.load_data(
            str(Path(__file__).parent / "data" / "galaxy_data.csv"), 
            label='galaxy_data')

        # Load some example simulated data
        self._application_handler.load_data(
            str(Path(__file__).parent / "data" / "hubble_simulation" / "example_student_measurements.csv"),
            label='student_measurements'
        )

        # Instantiate the initial viewers
        # Image viewer used for the 2D spectrum selection
        image_viewer = self._application_handler.new_data_viewer(
            BqplotImageView, data=None, show=False)

        # Scatter viewer used for the display of the measured galaxies
        hub_const_viewer = self._application_handler.new_data_viewer(
            BqplotScatterView, data=self.data_collection['example_student_measurements'], show=False)

        # Scatter viewer used for the galaxy selection
        gal_viewer = self._application_handler.new_data_viewer(
            BqplotScatterView, data=self.data_collection['galaxy_data'],
            show=False)

        # scatter_viewer.add_data(self.data_collection['galaxy_data'])
        gal_viewer.state.x_att = 'RA_deg'
        gal_viewer.state.y_att = 'Dec_deg'

        # TODO: Currently, the glue-wwt package requires qt binding even if we
        # only intend to use the juptyer viewer.
        wwt_viewer = self._application_handler.new_data_viewer(
            WWTJupyterViewer, data=self.data_collection['galaxy_data'], show=False)
        wwt_viewer.state.lon_att = 'RA_deg'
        wwt_viewer.state.lat_att = 'Dec_deg'

        # scatter_viewer_layout = vuetify_layout_factory(gal_viewer)

        # Store an internal collection of the glue viewer objects
        self._viewer_handlers = {
            'image_viewer': image_viewer, 
            'gal_viewer': gal_viewer,
            'hub_const_viewer': hub_const_viewer, 
            'wwt_viewer': wwt_viewer
        }

        # wwt_viewer_layout = vuetify_layout_factory(wwt_viewer)

        # Store an front-end accessible collection of renderable ipywidgets
        self.viewers = {
            'image_viewer': image_viewer.figure_widget, 
            'gal_viewer': gal_viewer.figure_widget, #scatter_viewer_layout,
            'hub_const_viewer': hub_const_viewer.figure_widget, 
            'wwt_viewer': wwt_viewer.figure_widget  # wwt_viewer_layout
        }

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

    def vue_add_data_to_viewers(self, viewer_ids):
        for viewer_id in viewer_ids:
            viewer = self._viewer_handlers[viewer_id]
            if viewer_id == 'hub_const_viewer':
                data = self.data_collection['example_student_measurements']
                viewer.add_data(data)
                viewer.x_att = 'RA_deg'
                viewer.y_att = 'Dec_deg'
            elif viewer_id == 'wwt_viewer':
                data = self.data_collection['galaxy_data']
                viewer.add_data(data)
                viewer.lon_att = 'RA_deg'
                viewer.lat_att = 'Dec_deg'

