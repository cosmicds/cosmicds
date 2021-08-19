from pathlib import Path

from echo import CallbackProperty
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

from .components.footer import Footer
# When we have multiple components, change above to
# from .components import *
from .components.viewer_layout import ViewerLayout
from .utils import load_template, update_figure_css
from .components.dialog import Dialog

# Within ipywidgets - update calls only happen in certain instances.
# Tom added this glue state to allow 2-way binding and force communication that we want explicitly controlled between front end and back end.
class ApplicationState(State):
    over_model = CallbackProperty(1)
    col_tab_model = CallbackProperty(0)
    est_model = CallbackProperty(0)

    gal_snackbar = CallbackProperty(0)
    dist_snackbar = CallbackProperty(0)
    marker_snackbar = CallbackProperty(0)
    vel_snackbar = CallbackProperty(0)
    data_ready_snackbar = CallbackProperty(0)

    gal_selected = CallbackProperty(0)
    dist_measured = CallbackProperty(0)
    marker_set = CallbackProperty(0)
    vel_measured = CallbackProperty(0)
    adddata_disabled = CallbackProperty(1)
    prev1_disabled = CallbackProperty(1)
    next1_disabled = CallbackProperty(1)

    haro_on = CallbackProperty("d-none")
    marker_on = CallbackProperty("d-none")
    galaxy_dist = CallbackProperty("")
    galaxy_vel = CallbackProperty("")


# Everything in this class is exposed directly to the app.vue.
class Application(VuetifyTemplate):
    _metadata = Dict({"mount_id": "content"}).tag(sync=True)
    state = GlueState().tag(sync=True)
    template = load_template("app.vue", __file__).tag(sync=True)
    viewers = Dict().tag(sync=True, **widget_serialization)
    items = List().tag(sync=True)
    vue_components = Dict().tag(sync=True, **widget_serialization)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the vue components through the ipyvuetify machinery. We add the
        # html tag we want and an instance of the component class as a 
        # key-value pair to the components dictionary.
        self.components = {'c-footer': Footer(self)
                        # THE FOLLOWING REPLACED WITH video_dialog.vue component in data/vue_components
                        #    'c-dialog-vel': Dialog(
                        #        self,
                        #        launch_button_text="Learn more",
                        #        title_text="How do we measure galaxy velocity?",
                        #        content_text="Verbiage about comparing observed & rest wavelengths of absorption/emission lines",
                        #        accept_button_text="Close"),
                        #    'c-dialog-age': Dialog(
                        #        self,
                        #        launch_button_text="Learn more",
                        #        title_text="How do we estimate age of the universe?",
                        #        content_text="Verbiage about how the slope of the Hubble plot is the inverse of the age of the universe.",
                        #        accept_button_text="Close")
        }

        self.state = ApplicationState()
        self._application_handler = JupyterApplication()
        
        # Load the galaxy position data
        # This adds the file to the glue data collection at the top level
        self._application_handler.load_data(
            str(Path(__file__).parent / "data" / "galaxy_data.csv"), 
            label='galaxy_data')

        # Load some example simulated data
        self._application_handler.load_data(
            str(Path(__file__).parent / "data" / "hubble_simulation" /
                "output" / "HubbleData_ClassSample.csv"),
            label='HubbleData_ClassSample')

        # Load some simulated age data
        self._application_handler.load_data(
            str(Path(__file__).parent / "data" / "hubble_simulation" /
                "output" / "HubbleSummary_Overall.csv"),
            label='HubbleSummary_Overall')

        # Instantiate the initial viewers
        # Image viewer used for the 2D spectrum selection
        image_viewer = self._application_handler.new_data_viewer(
            BqplotImageView, data=None, show=False)

        # Scatter viewer used for the display of the measured galaxy data
        hub_const_viewer = self._application_handler.new_data_viewer(
            BqplotScatterView, data=self.data_collection['HubbleData_ClassSample'], show=False)

        data = self.data_collection['HubbleData_ClassSample']
        hub_const_viewer.state.x_att = data.id['Distance']
        hub_const_viewer.state.y_att = data.id['Velocity']

        # Update the Hubble constant viewer CSS
        update_figure_css(hub_const_viewer,
                          style_path=Path(__file__).parent / "data" /
                                     "styles" / "default_scatter.json")

        # Scatter viewer used for the galaxy selection
        gal_viewer = self._application_handler.new_data_viewer(
            BqplotScatterView, data=self.data_collection['galaxy_data'],
            show=False)

        # Histogram viewer for age distribution
        age_distr_viewer = self._application_handler.new_data_viewer(
            BqplotHistogramView, data=self.data_collection['HubbleSummary_Overall'], show=False)

        # TO DO: Currently, the glue-wwt package requires qt binding even if we
        #  only intend to use the juptyer viewer.
        wwt_viewer = self._application_handler.new_data_viewer(
            WWTJupyterViewer, data=self.data_collection['galaxy_data'], show=False)

        data = self.data_collection['galaxy_data']
        wwt_viewer.state.lon_att = data.id['RA_deg']
        wwt_viewer.state.lat_att = data.id['Dec_deg']

        data = self.data_collection['HubbleSummary_Overall']
        age_distr_viewer.state.x_att = data.id['age']

        # scatter_viewer_layout = vuetify_layout_factory(gal_viewer)

        # Store an internal collection of the glue viewer objects
        self._viewer_handlers = {
            'image_viewer': image_viewer, 
            'gal_viewer': gal_viewer,
            'hub_const_viewer': hub_const_viewer, 
            'wwt_viewer': wwt_viewer,
            'age_distr_viewer': age_distr_viewer
        }

        # Store a front-end accessible collection of renderable ipywidgets
        self.viewers = {
            'image_viewer': ViewerLayout(image_viewer),
            'gal_viewer': ViewerLayout(gal_viewer),
            'hub_const_viewer': ViewerLayout(hub_const_viewer),
            'wwt_viewer': ViewerLayout(wwt_viewer),
            'age_distr_viewer': ViewerLayout(age_distr_viewer)
        }

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

    def vue_add_data_to_viewers(self, viewer_ids):
        for viewer_id in viewer_ids:
            viewer = self._viewer_handlers[viewer_id]
            if viewer_id == 'hub_const_viewer':
                data = self.data_collection['HubbleData_ClassSample']
                viewer.add_data(data)
                viewer.x_att = data.id['Distance']
                viewer.y_att = data.id['Velocity']
            elif viewer_id == 'wwt_viewer':
                data = self.data_collection['galaxy_data']
                viewer.add_data(data)
                viewer.lon_att = data.id['RA_deg']
                viewer.lat_att = data.id['Dec_deg']
            elif viewer_id == 'age_distr_viewer':
                data = self.data_collection['HubbleSummary_Overall']
                viewer.add_data(data)
                viewer.x_att = data.id['age']
            

