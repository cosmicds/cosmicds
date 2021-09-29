from os.path import join
from pathlib import Path

from astropy.modeling import models, fitting
from echo import CallbackProperty
from echo.core import add_callback
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
from .histogram_listener import HistogramListener
from .utils import age_in_gyr, extend_tool, line_mark, load_template, update_figure_css, vertical_line_mark
from .components.dialog import Dialog
from .viewers.spectrum_view import SpectrumView

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

    haro_on = CallbackProperty("d-flex")
    marker_on = CallbackProperty("d-none")
    galaxy_dist = CallbackProperty("")
    galaxy_vel = CallbackProperty("")

    draw_on = CallbackProperty(0)
    bestfit_on = CallbackProperty(0)

    hubble_comparison_selections = CallbackProperty([0])
    class_histogram_selections = CallbackProperty([0])
    alldata_histogram_selections = CallbackProperty([0,1])
    sandbox_histogram_selections = CallbackProperty([0])


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

        # State callbacks
        add_callback(self.state, 'hubble_comparison_selections', self._hubble_comparison_selection_update)
        add_callback(self.state, 'class_histogram_selections', self._class_histogram_selection_update)
        add_callback(self.state, 'alldata_histogram_selections', self._alldata_histogram_selection_update)
        add_callback(self.state, 'sandbox_histogram_selections', self._sandbox_histogram_selection_update)

        # Load the galaxy position data
        # This adds the file to the glue data collection at the top level
        data_dir = Path(__file__).parent / "data"
        output_dir = data_dir / "hubble_simulation" / "output"
        self._application_handler.load_data(str(data_dir / "galaxy_data.csv"), 
            label='galaxy_data')

        # Load some simulated measurements as summary data
        datasets =[
            "HubbleData_ClassSample",
            "HubbleData_All",
            "HubbleSummary_ClassSample",
            "HubbleSummary_Students",
            "HubbleSummary_Classes"
        ]
        for dataset in datasets:
            self._application_handler.load_data(join(output_dir, f"{dataset}.csv"), label=dataset)

        # Instantiate the initial viewers
        spectrum_viewer = self._application_handler.new_data_viewer(
            SpectrumView, data=None, show=False)

        self._application_handler.load_data(str(data_dir / "spectra" / 
            "SDSS_J143450.62+033842.5_S.ecsv"))

        spectrum_viewer.add_data("SDSS_J143450.62+033842.5_S")

        data = self.data_collection['SDSS_J143450.62+033842.5_S']
        # spectrum_viewer.state.x_att = data.id['wavelength']
        spectrum_viewer.layers[0].state.attribute = data.id['flux']

        # Scatter viewers used for the display of the measured galaxy data
        hub_viewers = [self._application_handler.new_data_viewer(BqplotScatterView, data=None, show=False) for _ in range(4)]
        hub_const_viewer, hub_fit_viewer, hub_comparison_viewer, hub_students_viewer = hub_viewers

        # Create a subset for the student
        class_data = self.data_collection['HubbleData_ClassSample']
        student_subset = class_data.new_subset(class_data.id["student_id"] == 1, label="Student 1")

        # Set up the scatter viewers
        style_path = str(Path(__file__).parent / "data" /
                                        "styles" / "default_scatter.json")
        for viewer in hub_viewers[:-1]:

            # Add the data from the first student
            viewer.add_subset(student_subset)

            # Set the x and y attributes of the viewer
            viewer.state.x_att = class_data.id['distance']
            viewer.state.y_att = class_data.id['velocity']

            # Update the viewer CSS
            update_figure_css(viewer, style_path=style_path)

        
        # Set up the viewer that will listen to the histogram
        hub_students_viewer.add_data(class_data)
        hub_students_viewer.state.x_att = class_data.id['distance']
        hub_students_viewer.state.y_att = class_data.id['velocity']
        update_figure_css(hub_students_viewer, style_path=style_path)

        # The Hubble comparison viewer should get the class and all public data as well
        all_data = self.data_collection['HubbleData_All']
        self._application_handler.add_link(class_data, 'distance', all_data, 'distance')
        self._application_handler.add_link(class_data, 'velocity', all_data, 'velocity')
        hub_comparison_viewer.add_data(class_data)
        hub_comparison_viewer.layers[-1].state.visible = False
        hub_comparison_viewer.add_data(all_data)
        hub_comparison_viewer.layers[-1].state.visible = False
        update_figure_css(hub_comparison_viewer, style_path=style_path)

        # For convenience, we attach the relevant data sets to the application instance
        self._class_data = class_data
        self._student_data = student_subset
        self._all_data = all_data

        # Link the age components of the summary data sets
        self._application_handler.add_link(self.data_collection['HubbleSummary_Students'], 'age', self.data_collection['HubbleSummary_Classes'], 'age')
        self._application_handler.add_link(self.data_collection['HubbleSummary_ClassSample'], 'age', self.data_collection['HubbleSummary_Classes'], 'age')

        # Scatter viewer used for the galaxy selection
        gal_viewer = self._application_handler.new_data_viewer(
            BqplotScatterView, data=self.data_collection['galaxy_data'],
            show=False)

        # Histogram viewers for age distribution
        age_distr_viewers = [self._application_handler.new_data_viewer(BqplotHistogramView, data=None, show=False) for _ in range(3)]
        class_distr_viewer, all_distr_viewer, sandbox_distr_viewer = age_distr_viewers

        # The class distribution viewer and the 'sandbox' histogram viewer
        # both need the data for students in the class
        for viewer in [class_distr_viewer, sandbox_distr_viewer]:
            viewer.add_data(self.data_collection["HubbleSummary_ClassSample"])
            viewer.layers[-1].state.color = 'orange'
            viewer.figure.marks[-1].opacities = [0.5]

        # The histogram viewer that shows the overall distribution
        # and the 'sandbox' histogram viewer both need the summary data
        # for all students and classes
        for viewer in [all_distr_viewer, sandbox_distr_viewer]:
            viewer.add_data(self.data_collection['HubbleSummary_Students'])
            viewer.layers[-1].state.color = 'blue'
            viewer.figure.marks[-1].opacities = [0.5]
            viewer.add_data(self.data_collection['HubbleSummary_Classes'])
            viewer.layers[-1].state.color = 'red'
            viewer.figure.marks[-1].opacities = [0.5]
            viewer.state.normalize = True
            viewer.state.y_min = 0
            viewer.state.y_max = 1
            viewer.state.hist_n_bin = 30

        # Set all of the histogram viewers to use age as the distribution attribute
        class_distr_viewer.state.x_att = self.data_collection["HubbleSummary_ClassSample"].id['age']
        all_distr_viewer.state.x_att = self.data_collection["HubbleSummary_Students"].id['age']
        sandbox_distr_viewer.state.x_att = self.data_collection["HubbleSummary_Students"].id['age']

        # Set up the listener to sync the histogram <--> scatter viewers
        meas_data = self.data_collection["HubbleData_ClassSample"]
        summ_data = self.data_collection["HubbleSummary_ClassSample"]
        students_scatter_subset = meas_data.new_subset(label="Scatter students")
        
        # Set up the functionality for the histogram <---> scatter sync
        # We add a listener for when a subset is modified/created on 
        # the histogram viewer as well as extend the xrange tool for the 
        # histogram to always affect this subset
        hub_students_viewer.layers[-1].state.color = "#ff0000"
        self._histogram_listener = HistogramListener(self,
                                                     summ_data,
                                                     students_scatter_subset,
                                                     ['class_distr_viewer'],
                                                     ['hub_students_viewer'],
                                                     listen=False)

        def hist_selection_activate():
            if self._histogram_listener.source is not None:
                self.session.edit_subset_mode.edit_subset = [self._histogram_listener.source.group]
            self._histogram_listener.listen()
        def hist_selection_deactivate():
            self.session.edit_subset_mode.edit_subset = []
            self._histogram_listener.ignore()
        extend_tool(class_distr_viewer, 'bqplot:xrange', hist_selection_activate, hist_selection_deactivate)

        # TO DO: Currently, the glue-wwt package requires qt binding even if we
        #  only intend to use the juptyer viewer.
        wwt_viewer = self._application_handler.new_data_viewer(
            WWTJupyterViewer, data=self.data_collection['galaxy_data'], show=False)

        data = self.data_collection['galaxy_data']
        wwt_viewer.state.lon_att = data.id['RA_deg']
        wwt_viewer.state.lat_att = data.id['Dec_deg']

        # Any lines that we've obtained from fitting
        # Entries have the form (line, data label)
        # These are keyed by viewer id
        self._fit_lines = {}

        # The slopes that we've fit to any data sets
        # This is keyed by the label of the data
        self._fit_slopes = {}

        # Any vertical line marks on histograms
        # keyed by viewer id
        self._histogram_lines = {}

        # scatter_viewer_layout = vuetify_layout_factory(gal_viewer)

        # Store an internal collection of the glue viewer objects
        self._viewer_handlers = {
            'spectrum_viewer': spectrum_viewer, 
            'gal_viewer': gal_viewer,
            'hub_const_viewer': hub_const_viewer,
            'hub_comparison_viewer': hub_comparison_viewer,
            'hub_students_viewer': hub_students_viewer,
            'hub_fit_viewer': hub_fit_viewer,
            'wwt_viewer': wwt_viewer,
            'class_distr_viewer': class_distr_viewer,
            'all_distr_viewer': all_distr_viewer,
            'sandbox_distr_viewer': sandbox_distr_viewer
        }

        # Store a front-end accessible collection of renderable ipywidgets
        self.viewers = { k : ViewerLayout(v) for k, v in self._viewer_handlers.items() }

        # Make sure that the initial layer visibilities match the state
        self._class_histogram_selection_update(self.state.class_histogram_selections)
        self._alldata_histogram_selection_update(self.state.alldata_histogram_selections)
        self._sandbox_histogram_selection_update(self.state.sandbox_histogram_selections)

        self._application_handler.set_subset_mode('replace')

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

    #def vue_fit_lines(self, viewer_id, data_ids=None, clear_others=False, aggregate=False):
    def vue_fit_lines(self, args):
        """
        This function handles line fitting, with the specifics of the fitting
        controlled by the arguments.

        Parameters
        ----------
        args: dict
            A dictionary of arguments, with following entries:

        viewer_id : str
            The identifier for the viewer to use.
        layers : List[int]
            (Optional) A list of the indices of the layers that should be fit to. 
            If not specified, a line is fit for every layer present in 
            the viewer.
        clear_others: bool
            (Optional) If true, all old lines present on this viewer will be cleared.
            Otherwise, only old lines for the selected data ids will be cleared;
            lines for other layers will be left as they are. Default is False.
        aggregate: bool
            (Optional) If true, the data for all specified layers is concatenated and a
            single fit is done for the combined data. Otherwise, a separate fit
            is done for each layer. Default is False.
        """

        viewer_id = args['viewer_id']
        layer_indices = args.get('layers')
        clear_others = args.get('clear_others') or False
        aggregate = args.get('aggregate') or False
        viewer = self._viewer_handlers[viewer_id]

        if layer_indices is None:
            layer_indices = list(range(len(viewer.layers)))
        layers = [layer for index, layer in enumerate(viewer.layers) if layer.state.visible and index in layer_indices]
        
        if aggregate:
            self._fit_lines_aggregate(viewer_id, layers, clear_others)
        else:
            self._fit_lines_layers(viewer_id, layers, clear_others)

    def _fit_lines_layers(self, viewer_id, layers, clear_others=False):
        viewer = self._viewer_handlers[viewer_id]
        figure = viewer.figure

        data_labels = [layer.state.layer.label for layer in layers]

        lines, labels = [], []
        for layer in layers:

            # Get the data (which may actually be a Data object,
            # or represent a subset
            data = layer.state.layer

            # Do the line fit
            x_arr = data[viewer.state.x_att]
            y_arr = data[viewer.state.y_att]
            fit = fitting.LinearLSQFitter()
            line_init = models.Linear1D(intercept=0, fixed={'intercept':True})
            fitted_line = fit(line_init, x_arr, y_arr)
            x = [0, 2*viewer.state.x_max] # For now, the line spans from 0 to twice the edge of the viewer
            y = fitted_line(x)

            # Create the fit line object
            # Keep track of this line and its slope
            start_x, end_x = x
            start_y, end_y = y
            line = line_mark(layer, start_x, start_y, end_x, end_y, layer.state.color)
            lines.append(line)
            labels.append(data.label)
            
            # Keep track of this slope for later use
            self._fit_slopes[data.label] = fitted_line.slope.value

        # Since the glupyter viewer doesn't have an option for lines
        # we just draw the fit lines directly onto the bqplot figure
        # If we previously drew any lines in this viewer, remove them
        old_items = self._fit_lines.get(viewer_id, [])
        to_clear, to_keep = [], []
        for item in old_items:
            if clear_others or (item[1] in data_labels):
                to_clear.append(item)
            else:
                to_keep.append(item)
        marks_to_clear = [x[0] for x in to_clear]
        marks_to_keep = [x for x in figure.marks if x not in marks_to_clear]
        figure.marks = marks_to_keep + lines
        self._fit_lines[viewer_id] = to_keep + list(zip(lines, labels))

    def _fit_lines_aggregate(self, viewer_id, layers, clear_others=False):
        viewer = self._viewer_handlers[viewer_id]
        figure = viewer.figure

        x, y = [], []
        for layer in layers:

            # Get the data (which may actually be a Data object,
            # or represent a subset
            data = layer.state.layer

            # Do the line fit
            x_arr = data[viewer.state.x_att]
            y_arr = data[viewer.state.y_att]
            x.extend(list(x_arr))
            y.extend(list(y_arr))

        fit = fitting.LinearLSQFitter()
        line_init = models.Linear1D(intercept=0, fixed={'intercept':True})
        fitted_line = fit(line_init, x, y)
        x = [0, 2*viewer.state.x_max] # For now, the line spans from 0 to twice the edge of the viewer
        y = fitted_line(x)

        # Create the fit line object
        # Keep track of this line and its slope
        start_x, end_x = x
        start_y, end_y = y
        line = line_mark(layers[0], start_x, start_y, end_x, end_y, 'black')
        self._fit_slopes['aggregate_%s' % viewer_id] = fitted_line.slope.value

         # Since the glupyter viewer doesn't have an option for lines
        # we just draw the fit line directly onto the bqplot figure
        # If we previously drew any lines in this viewer, remove them
        old_items = self._fit_lines.get(viewer_id, [])
        to_clear, to_keep = [], []
        for item in old_items:
            if clear_others or (item[1] == 'aggregate'):
                to_clear.append(item)
            else:
                to_keep.append(item)
        marks_to_clear = [x[0] for x in to_clear]
        marks_to_keep = [x for x in figure.marks if x not in marks_to_clear]
        figure.marks = marks_to_keep + [line]
        self._fit_lines[viewer_id] = to_keep + [(line, 'aggregate')]

    def vue_clear_lines(self, viewer_id):
        """
        "Clears all fit lines for the given viewer.
        """
        viewer = self._viewer_handlers[viewer_id]
        figure = viewer.figure

        old_items = self._fit_lines.get(viewer_id, [])
        old_marks = [x[0] for x in old_items]

        figure.marks = [mark for mark in figure.marks if mark not in old_marks]
        self._fit_lines[viewer_id] = []

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

    def _hubble_comparison_selection_update(self, selections):
        # Indices:
        # 0: Student's data
        # 1: Their class's data
        # 2: All public data
        viewer_id = 'hub_comparison_viewer'
        viewer = self._viewer_handlers[viewer_id]
        data = [self._student_data, self._class_data, self._all_data]
        labels = [x.label for (i,x) in enumerate(data) if i in selections]

        for layer in viewer.layers:
            layer.state.visible = layer.state.layer.label in labels
        
        # We only want to show lines for the layers that are visible
        line_info = self._fit_lines.get(viewer_id, [])
        all_lines = [x[0] for x in line_info]
        
        figure = viewer.figure
        not_lines = [mark for mark in figure.marks if mark not in all_lines]
        lines = [x[0] for x in line_info if x[1] in labels]
        figure.marks = not_lines + lines

    def _histogram_selection_update(self, selections, viewer_id, line_options=[], layer_mapping=None):
        """
        Callback function to be executed when the selections corresponding to one of
        the histogram viewers is changed.

        Parameters
        ----------
        selections : List[int]
            The indices of the selected options.
        viewer_id : str
            The identifier for the viewer to use.
        layer_mapping : Dict[int,int]
            (Optional) A dictionary mapping the indices of glue layers to the selection
            indices. If not given, the layer at a given index will be mapped to
            the selection option at the same index.
        line_options: List[Tuple[int, float, str]]
            (Optional) A list of tuple of options (index, slope, color) for the vertical
            lines to be plotted.
        """
        viewer = self._viewer_handlers[viewer_id]
        first_layer = viewer.layers[0]

        layer_mapping = layer_mapping or { x : x for x in range(len(viewer.layers)) }
        for index, layer in enumerate(viewer.layers):
            layer.state.visible = layer_mapping.get(index, -1) in selections

        lines = []
        for index, slope, color in line_options:
            if index in selections and slope is not None:
                age = age_in_gyr(slope)
                line = vertical_line_mark(first_layer, age, color)
                lines.append(line)

        figure = viewer.figure
        old_lines = self._histogram_lines.get(viewer_id, [])
        figure.marks = [mark for mark in figure.marks if not mark in old_lines] + lines
        self._histogram_lines[viewer_id] = lines
            
    def _class_histogram_selection_update(self, selections):
        """
        Specialization of _histogram_selection_update for the case of the class histogram.

        Parameters
        ----------
        selections : List[int]
            The indices of the selected options. The indices in this case represent:
            * 0: Individual students (glue layer)
            * 1: Student's selected subset (glue layer) - only if student has made selection
            * 1 or 2: Student's value (line mark)
            * 2 or 3: Class's value (line mark)
        """

        line_options = [
            (1, self.student_slope, 'blue'),
            (2, self.class_slope, 'green')
        ]
        layer_mapping = { 0 : 0, 1 : 0 } # We hide a selected subset if the glue layer is hidden
        print(selections)
        self._histogram_selection_update(selections, 'class_distr_viewer',
            layer_mapping=layer_mapping, line_options=line_options)
    
    def _alldata_histogram_selection_update(self, selections):
        """
        Specialization of _histogram_selection_update for the case of the histogram of all data.

        Parameters
        ----------
        selections : List[int]
            The indices of the selected options. The indices in this case represent:
            * 0: All students (glue layer)
            * 1: All students (glue layer)
        """
        self._histogram_selection_update(selections, 'all_distr_viewer')
    
    def _sandbox_histogram_selection_update(self, selections):
        """
        Specialization of _histogram_selection_update for the case of the final 'sandbox' histogram.

        Parameters
        ----------
        selections : List[int]
            The indices of the selected options. The indices in this case represent:
            * 0: Students in the class (glue layer)
            * 1: All students (glue layer)
            * 2: Students from all classes (glue layer)
            * 3: This class's age (line mark)
            * 4: Age from all data (line mark)
            * 5: Student's age (line mark)
        """
        line_options = [
            (3, self.class_slope, 'purple'),
            (4, self.all_slope, 'green'),
            (5, self.student_slope, 'black')
        ]
        self._histogram_selection_update(selections, 'sandbox_distr_viewer', line_options=line_options)

    def vue_clear_histogram_selection(self, _args):
        toolbar = self._viewer_handlers['class_distr_viewer'].toolbar
        toolbar.active_tool = None
        self._histogram_listener.clear_subset()

    # These three properties provide convenient access to the slopes of the the fit lines
    # for the student's data, the class's data, and all of the data
    @property
    def student_slope(self):
        return self._fit_slopes.get(self._student_data.label)

    @property
    def class_slope(self):
        return self._fit_slopes.get(self._class_data.label)

    @property
    def all_slope(self):
        return self._fit_slopes.get(self._all_data.label)
