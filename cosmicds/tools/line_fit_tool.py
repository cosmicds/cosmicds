from astropy.modeling import models, fitting
from glue.config import viewer_tool
from glue.core import HubListener
from glue.core.message import (DataCollectionDeleteMessage, DataUpdateMessage,
                               SubsetMessage, SubsetCreateMessage, SubsetUpdateMessage)
from glue.core.exceptions import IncompatibleAttribute
from glue_jupyter.bqplot.common.tools import Tool
from numpy import isnan
from numpy.linalg import LinAlgError
from traitlets import Unicode, HasTraits

from cosmicds.stories.hubbles_law.utils import line_mark, age_in_gyr_simple

@viewer_tool
class LineFitTool(Tool, HubListener, HasTraits):

    tool_id = 'cds:linefit'
    action_text = 'Fit lines'
    tool_tip = Unicode().tag(sync=True)
    mdi_icon = 'mdi-chart-timeline-variant'

    inactive_tool_tip = 'Fit lines to data'
    active_tool_tip = 'Clear fit lines'
    
    def __init__(self, viewer, **kwargs):
        super().__init__(viewer, **kwargs)
        self.lines = {}
        self.slopes = {}
        self.tool_tip = self.inactive_tool_tip
        self.active = False
        #self._data_filter = lambda message: message.data.label in self.layer_labels
        #self._subset_filter = lambda message: message.subset.label in self.layer_labels and message.data.label in self.layer_labels
        self.hub.subscribe(self, DataCollectionDeleteMessage,
                           handler=self._on_data_collection_deleted, filter=self._data_collection_filter)
        self.hub.subscribe(self, DataUpdateMessage,
                           handler=self._on_layer_updated, filter=self._update_filter)
        # self.hub.subscribe(self, NumericalDataChangedMessage,
        #                    handler=self._on_layer_updated, filter=self._data_filter)
        self.hub.subscribe(self, SubsetCreateMessage,
                           handler=self._on_subset_created, filter=self._create_filter)
        self.hub.subscribe(self, SubsetUpdateMessage,
                           handler=self._on_layer_updated, filter=self._update_filter)


    def _data_collection_filter(self, msg):
        return msg.data in self.lines.keys()

    def _create_filter(self, msg):
        return msg.subset.data in self.lines.keys()

    def _update_filter(self, msg):
        subset_message = isinstance(msg, SubsetMessage)
        subset = msg.subset if subset_message else None
        data = subset.data if subset_message else msg.data
        return (data in self.lines.keys() or subset in self.lines.keys()) \
            and msg.attribute in [self.viewer.state.x_att, self.viewer.state.y_att]

    def _on_subset_created(self, _msg):
        if self.active:
            self.refresh()

    def _on_data_collection_deleted(self, msg):
        remove = [layer for layer in self.lines.keys() if layer.state.layer == msg.data]
        lines = [self.lines[x] for x in remove]
        self.figure.marks = [mark for mark in self.figure.marks if mark not in lines]
        for layer in remove:
            self._remove_line(layer)

    def _on_layer_updated(self, msg):
        data = msg.subset if isinstance(msg, SubsetMessage) else msg.data
        for layer in self.visible_layers:
            if layer.state.layer == data:
                self._update_fit_line(layer)
                return

    @property
    def figure(self):
        return self.viewer.figure

    @property
    def dc(self):
        return self.viewer.session.data_collection

    @property
    def visible_layers(self):
        return filter(lambda layer: layer.state.visible, self.viewer.layers)

    @property
    def layer_labels(self):
        return [x.state.layer.label for x in self.viewer.layers]

    @property
    def hub(self):
        return self.viewer.session.hub

    def _fit_line(self, layer):
        data = layer.state.layer
        x = data[self.viewer.state.x_att]
        y = data[self.viewer.state.y_att]
        fit = fitting.LinearLSQFitter()
        line_init = models.Linear1D(intercept=0, fixed={'intercept':True})
        fitted_line = fit(line_init, x, y)
        return fitted_line

    def _create_fit_line(self, layer):

        # Do the fit
        fit_line = self._fit_line(layer)
    
        # Create the fit line object
        # Keep track of this line and its slope # For now, the line spans from 0 to twice the edge of the viewer
        y = fit_line(self.x_range)
        start_x, end_x = self.x_range
        start_y, end_y = y
        slope = fit_line.slope.value
        age = age_in_gyr_simple(slope)
        label = self.label(slope, age)
        color = layer.state.color if layer.state.color != '0.35' else 'black'
        line = line_mark(layer, start_x, start_y, end_x, end_y, color, label)
        return line, slope

    def _update_fit_line(self, layer):
        data = layer.state.layer
        if data in self.lines.keys():
            fit_line = self._fit_line(layer)
            mark = self.lines[data]
            mark.x = self.x_range
            mark.y = fit_line(self.x_range)
            slope = fit_line.slope.value
            age = age_in_gyr_simple(slope)
            self.slopes[data] = slope
            label = self.label(slope, age)
            is_label = label is not None
            mark.display_legend = is_label
            mark.labels = [label] if is_label else []
        else:
            self._fit_to_layer(layer)

    def activate(self):
        if not self.active:
            self._fit_to_layers()
            self.tool_tip = self.active_tool_tip
        else:
            self._clear_lines()
            self.tool_tip = self.inactive_tool_tip
        self.active = not self.active

    def _fit_to_layer(self, layer, add_marks=True):
        try:
            line, slope = self._create_fit_line(layer)
            data = layer.state.layer
            self.lines[data] = line
            self.slopes[data] = slope
        except (IncompatibleAttribute, LinAlgError, SystemError):
            pass

        if add_marks:
            self.figure.marks = self.figure.marks + [line]

    def _fit_to_layers(self):

        marks_to_keep = [mark for mark in self.figure.marks if mark not in self.line_marks]

        self.lines = {}
        self.slopes = {}
        for layer in self.visible_layers:
            self._fit_to_layer(layer, add_marks=False)

        self.figure.marks = marks_to_keep + list(self.line_marks)

    def _remove_line(self, layer):
        data = layer.state.layer
        line = self.lines.get(data, None)
        del self.lines[data]
        del self.slopes[data]
        self.figure.marks = [mark for mark in self.figure.marks if mark != line]

    def _clear_lines(self):
        self.figure.marks = [mark for mark in self.figure.marks if mark not in self.line_marks]
        self.lines = {}
        self.slopes = {}

    def refresh(self):
        self._fit_to_layers()

    def label(self, slope, age):
        return 'H0=%.0f km/s/Mpc;  %.0f Gyr' % (slope, age) if not isnan(slope) else None
            
    @property
    def line_marks(self):
        return self.lines.values()

    @property
    def x_range(self):
        return [0, 2 * self.viewer.state.x_max]


    