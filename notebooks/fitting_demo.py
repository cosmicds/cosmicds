from pathlib import Path
from re import TEMPLATE

from astropy.modeling import models, fitting
from bqplot_image_gl import LinesGL
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
from numpy import unique
from traitlets import Dict, List

from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from traitlets import Dict, Instance
from ipywidgets import DOMWidget
from traitlets import Unicode

import sys
sys.path.append('../cosmicds/components/viewer_layout')

class ViewerLayout(VuetifyTemplate):
    TEMPLATE_STR = """
    <template>
        <v-card flat>
            <v-toolbar flat short>
            <v-toolbar-items>
                <jupyter-widget :widget="controls.toolbar_selection_tools"></jupyter-widget>
            </v-toolbar-items>
            </v-toolbar>
            <jupyter-widget :style="css_style" :widget="figure"></jupyter-widget>
        </v-card>
    </template>
    """
    template = Unicode(TEMPLATE_STR).tag(sync=True)
    controls = Dict().tag(sync=True, **widget_serialization)
    figure = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)
    css_style = Dict().tag(sync=True)

    def __init__(self, viewer, style=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controls = dict(
            toolbar_selection_tools=viewer.toolbar_selection_tools,
            toolbar_selection_mode=viewer.toolbar_selection_mode,
            toolbar_active_subset=viewer.toolbar_active_subset)

        self.css_style = style or {'height': '300px'}
        self.figure = viewer.figure_widget

class FittingTest(VuetifyTemplate):
    _metadata = Dict({"mount_id": "content"}).tag(sync=True)
    state = GlueState().tag(sync=True)

    with open('fitting_demo.vue', 'r') as f:
        TEMPLATE_STR = f.read()
    template = Unicode(TEMPLATE_STR).tag(sync=True)
    viewers = Dict().tag(sync=True, **widget_serialization)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._application_handler = JupyterApplication()

        # Load some example simulated data
        self._application_handler.load_data(
            str(Path(__file__).parent.parent / "cosmicds" / "data" / "hubble_simulation" /
                "output" / "HubbleData_ClassSample.csv"),
            label='HubbleData_ClassSample')

        # Load some simulated age data
        self._application_handler.load_data(
            str(Path(__file__).parent.parent / "cosmicds" / "data" / "hubble_simulation" /
                "output" / "HubbleSummary_Overall.csv"),
            label='HubbleSummary_Overall')

        viewer = self._application_handler.new_data_viewer(
            BqplotScatterView, data=None, show=False
        )
        viewer.figure_widget.background_style = {"fill": "#e3f2f4"}

        # Create a subset for each student
        student_data = self._application_handler.data_collection['HubbleData_ClassSample']
        student_subsets = [student_data.new_subset(student_data.id["StudentNum"] == x, label="Student %d" % x) for x in unique(student_data["StudentNum"])]

        for i in range(4):
            viewer.add_subset(student_subsets[i])

        viewer.state.x_att = student_data.id['Distance']
        viewer.state.y_att = student_data.id['Velocity']

        self._viewer_handlers = {
            'viewer': viewer
        }

        self.viewers = { k : ViewerLayout(v) for k,v in self._viewer_handlers.items() }

        # Any lines that we've obtained from fitting
        # Entries have the form (line, data UUID)
        # These are keyed by viewer id
        self._fit_lines = {}

        # The slopes that we've fit to any data sets
        # This is keyed by the UUID of the data
        self._fit_slopes = {}

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
        layer_indices : List[int]
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

        data_ids = [layer.state.layer.uuid for layer in layers]

        lines, ids = [], []
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
            line = LinesGL(x=list(x), y=list(y), scales=layer.image.scales, colors=[layer.state.color], labels_visibility='label')
            lines.append(line)
            ids.append(data.uuid)
            
            # Keep track of this slope for later use
            self._fit_slopes[data.uuid] = fitted_line.slope.value

        # Since the glupyter viewer doesn't have an option for lines
        # we just draw the fit lines directly onto the bqplot figure
        # If we previously drew any lines in this viewer, remove them
        old_items = self._fit_lines.get(viewer_id, [])
        to_clear, to_keep = [], []
        for item in old_items:
            if clear_others or (item[1] in data_ids):
                to_clear.append(item)
            else:
                to_keep.append(item)
        marks_to_clear = [x[0] for x in to_clear]
        marks_to_keep = [x for x in figure.marks if x not in marks_to_clear]
        figure.marks = marks_to_keep + lines
        self._fit_lines[viewer_id] = to_keep + list(zip(lines, ids))

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
        line = LinesGL(x=list(x), y=list(y), scales=layers[0].image.scales, colors=['black'], labels_visibility='label')
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

    @property
    def data_collection(self):
        """
        Underlying glue-jupyter application data collection instance.
        """
        return self._application_handler.data_collection
