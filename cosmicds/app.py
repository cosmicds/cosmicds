from pathlib import Path

from astropy.modeling import models, fitting
from bqplot_image_gl import LinesGL
from echo import CallbackProperty
from glue.core.data import Subset
from glue.core.state_objects import State
from glue_jupyter.app import JupyterApplication
from glue_jupyter.bqplot.histogram import BqplotHistogramView
from glue_jupyter.bqplot.image import BqplotImageView
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.state_traitlets_helpers import GlueState
from glue_wwt.viewer.jupyter_viewer import WWTJupyterViewer
from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from numpy import unique
from traitlets import Dict, List

from .components.footer import Footer
from .components.viewer_layout import ViewerLayout
from .utils import load_template, update_figure_css
from .components.dialog import Dialog


class ApplicationState(State):
    over_model = CallbackProperty(1)
    col_tab_model = CallbackProperty(0)
    est_model = CallbackProperty(0)
    snackbar = CallbackProperty(0) #I think this initializes it in vue.app with a value=0. When I tried CallbackProperty(1), the app initializes with the snackbar already open.


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
        self.components = {'c-footer': Footer(self),
                           'c-dialog-vel': Dialog(
                               self,
                               launch_button_text="Learn more",
                               title_text="How do we measure galaxy velocity?",
                               content_text="Verbiage about comparing observed & rest wavelengths of absorption/emission lines",
                               accept_button_text="Close"),
                           'c-dialog-age': Dialog(
                               self,
                               launch_button_text="Learn more",
                               title_text="How do we estimate age of the universe?",
                               content_text="Verbiage about how the slope of the Hubble plot is the inverse of the age of the universe.",
                               accept_button_text="Close")}

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
            BqplotScatterView, data=None, show=False)
        hub_fit_viewer = self._application_handler.new_data_viewer(
            BqplotScatterView, data=None, show=False)

        # Create a subset for each student
        student_data = self.data_collection['HubbleData_ClassSample']
        student_subsets = [student_data.new_subset(student_data.id["StudentNum"] == x, label="Student %d" % x) for x in unique(student_data["StudentNum"])]

        # Set up the scatter viewers
        style_path = str(Path(__file__).parent / "data" /
                                        "styles" / "default_scatter.json")
        for viewer in [hub_const_viewer, hub_fit_viewer]:

            # Add the data from the first student
            viewer.add_subset(student_subsets[0])

            # Set the x and y attributes of the viewer
            viewer.state.x_att = student_data.id['Distance']
            viewer.state.y_att = student_data.id['Velocity']

            # Update the viewer CSS
            update_figure_css(viewer, style_path=style_path)

        # Scatter viewer used for the galaxy selection
        gal_viewer = self._application_handler.new_data_viewer(
            BqplotScatterView, data=self.data_collection['galaxy_data'],
            show=False)

        # Histogram viewer for age distribution
        age_distr_viewer = self._application_handler.new_data_viewer(
            BqplotHistogramView, data=self.data_collection['HubbleSummary_Overall'], show=False)

        # TODO: Currently, the glue-wwt package requires qt binding even if we
        #  only intend to use the juptyer viewer.
        wwt_viewer = self._application_handler.new_data_viewer(
            WWTJupyterViewer, data=self.data_collection['galaxy_data'], show=False)

        data = self.data_collection['galaxy_data']
        wwt_viewer.state.lon_att = data.id['RA_deg']
        wwt_viewer.state.lat_att = data.id['Dec_deg']

        data = self.data_collection['HubbleSummary_Overall']
        age_distr_viewer.state.x_att = data.id['age']

        # Any lines that we've obtained from fitting, and their slopes
        # This is keyed by viewer id
        self.fit_info = {}

        # scatter_viewer_layout = vuetify_layout_factory(gal_viewer)

        # Store an internal collection of the glue viewer objects
        self._viewer_handlers = {
            'image_viewer': image_viewer, 
            'gal_viewer': gal_viewer,
            'hub_const_viewer': hub_const_viewer,
            'hub_fit_viewer': hub_fit_viewer,
            'wwt_viewer': wwt_viewer,
            'age_distr_viewer': age_distr_viewer
        }

        # Store a front-end accessible collection of renderable ipywidgets
        self.viewers = {
            'image_viewer': ViewerLayout(image_viewer),
            'gal_viewer': ViewerLayout(gal_viewer),
            'hub_const_viewer': ViewerLayout(hub_const_viewer),
            'hub_fit_viewer': ViewerLayout(hub_fit_viewer),
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

    def vue_fit_lines(self, viewer_id):
        viewer = self._viewer_handlers[viewer_id]
        figure = self.viewers[viewer_id].figure

        lines, slopes = [], []
        for layer in viewer.layers:

            # Only draw lines for visible layers
            if not layer.state.visible:
                continue

            # Get the data
            # We want to distinguish whether this layer corresponds
            # to a Subset or not
            data = layer.state.layer
            if isinstance(data, Subset):
                subset = data
                data = subset.data
            else:
                subset = None
            subset_layer = subset is not None

            # Do the line fit
            values = subset if subset_layer else data
            x_arr = values[viewer.state.x_att]
            y_arr = values[viewer.state.y_att]
            fit = fitting.LinearLSQFitter()
            line_init = models.Linear1D(intercept=0, fixed={'intercept':True})
            fitted_line = fit(line_init, x_arr, y_arr)
            x = sorted(list(x_arr))
            x = [0] + x + [2*x[-1]] # For now, the line spans from 0 to twice the maximum value of x
            y = fitted_line(x)

            # Create the fit line object
            # Keep track of this line and its slope
            line = LinesGL(x=list(x), y=list(y), scales=layer.image.scales, colors=[layer.state.color], labels_visibility='label')
            lines.append(line)
            slopes.append(fitted_line.slope.value)

        # Since the glupyter viewer doesn't have an option for lines
        # we just draw the fit line directly onto the bqplot figure
        # If we previously drew any lines in this viewer, remove them
        old_viewer_marks = [x[0] for x in self.fit_info.get(viewer_id, [])]
        marks_to_keep = [x for x in figure.marks if x not in old_viewer_marks]
        figure.marks = marks_to_keep + lines

        # Add the lines and slopes to the app dictionaries
        self.fit_info[viewer_id] = list(zip(lines, slopes))

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
            

