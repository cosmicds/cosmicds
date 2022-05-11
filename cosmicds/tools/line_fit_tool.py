from astropy.modeling import models, fitting
from glue.config import viewer_tool
from glue.core import HubListener
from glue.core.message import (DataCollectionAddMessage,
                               DataCollectionDeleteMessage, DataUpdateMessage,
                               NumericalDataChangedMessage, SubsetUpdateMessage)
from glue_jupyter.bqplot.common.tools import Tool
from numpy import isnan

from cosmicds.stories.hubbles_law.utils import line_mark

@viewer_tool
class LineFitTool(Tool, HubListener):

    tool_id = 'cds:linefit'
    action_text = 'Fit lines'
    tool_tip = 'Fit lines to data'
    mdi_icon = 'mdi-chart-timeline-variant'
    
    def __init__(self, viewer, **kwargs):
        super().__init__(viewer, **kwargs)
        self.lines = {}
        self.slopes = {}
        #self._data_filter = lambda message: message.data.label in self.layer_labels
        #self._subset_filter = lambda message: message.subset.label in self.layer_labels and message.data.label in self.layer_labels
        # self.hub.subscribe(self, DataCollectionAddMessage,
        #                    handler=self._on_data_collection_added, filter=self._data_filter)
        # self.hub.subscribe(self, DataCollectionDeleteMessage,
        #                    handler=self._on_data_collection_deleted, filter=self._data_filter)
        # self.hub.subscribe(self, DataUpdateMessage,
        #                    handler=self._on_layer_updated, filter=self._data_filter)
        # self.hub.subscribe(self, NumericalDataChangedMessage,
        #                    handler=self._on_layer_updated, filter=self._data_filter)
        # self.hub.subscribe(self, SubsetUpdateMessage,
        #                    handler=self._on_layer_updated, filter=self._subset_filter)

    @property
    def dc(self):
        return self.viewer.session.data_collection

    @property
    def layer_labels(self):
        return [x.state.layer.label for x in self.viewer.layers]

    @property
    def hub(self):
        return self.viewer.session.hub

    def _create_fit_line(self, layer):
        data = layer.state.layer
        x = data[self.viewer.state.x_att]
        y = data[self.viewer.state.y_att]
        fit = fitting.LinearLSQFitter()
        line_init = models.Linear1D(intercept=0, fixed={'intercept':True})
        fitted_line = fit(line_init, x, y)
        x = [0, 2 * self.viewer.state.x_max] # For now, the line spans from 0 to twice the edge of the viewer
        y = fitted_line(x)
    
        # Create the fit line object
        # Keep track of this line and its slope
        start_x, end_x = x
        start_y, end_y = y
        slope = fitted_line.slope.value
        label = 'Slope = %.0f km / s / Mpc' % slope if not isnan(slope) else None
        color = layer.state.color if layer.state.color != '0.35' else 'black'
        line = line_mark(layer, start_x, start_y, end_x, end_y, color, label)
        return line, slope

    def activate(self):
        self._fit_to_layers()

    def deactivate(self):
        self._clear_lines()

    def _fit_to_layers(self):

        figure = self.viewer.figure
        marks_to_keep = [mark for mark in figure.marks if mark not in self.lines.keys()]

        self.lines = {}
        self.slopes = {}
        for layer in self.viewer.layers:
            label = layer.state.layer.label
            line, slope = self._create_fit_line(layer)
            self.lines[label] = line
            self.slopes[label] = slope

        figure.marks = marks_to_keep + list(self.line_marks)


    def _clear_lines(self):
        figure = self.viewer.figure
        figure.marks = [mark for mark in figure.marks if mark not in self.lines.keys()]
        self.lines = {}
        self.slopes = {}

    @property
    def line_marks(self):
        return self.lines.values()
            
            


    