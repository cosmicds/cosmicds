from astropy.modeling import models, fitting
from glue.config import viewer_tool
from glue.core import HubListener
from glue.core.message import (DataCollectionAddMessage,
                               DataCollectionDeleteMessage, DataUpdateMessage,
                               NumericalDataChangedMessage, SubsetUpdateMessage)
from glue_jupyter.bqplot.common.tools import Tool

from cosmicds.stories.hubbles_law.utils import line_mark

@viewer_tool
class LineFitTool(Tool, HubListener):

    tool_id = 'hubble:linefit'
    action_text = 'Fit lines'
    tool_tip = 'Fit lines to data'
    
    def __init__(self, viewer, **kwargs):
        super().__init__(viewer, **kwargs)
        self._data_filter = lambda message: message.data.label in self.layer_labels
        self._subset_filter = lambda message: message.subset.label in self.layer_labels and message.data.label in self.layer_labels
        self.hub.subscribe(self, DataCollectionAddMessage,
                           handler=self._on_data_collection_added, filter=self._data_filter)
        self.hub.subscribe(self, DataCollectionDeleteMessage,
                           handler=self._on_data_collection_deleted, filter=self._data_filter)
        self.hub.subscribe(self, DataUpdateMessage,
                           handler=self._on_layer_updated, filter=self._data_filter)
        self.hub.subscribe(self, NumericalDataChangedMessage,
                           handler=self._on_layer_updated, filter=self._data_filter)
        self.hub.subscribe(self, SubsetUpdateMessage,
                           handler=self._on_layer_updated, filter=self._subset_filter)

    @property
    def dc(self):
        return self.viewer.session.data_collection

    @property
    def layer_labels(self):
        return [x.label for x in self.viewer.layers]

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
        slope_value = fitted_line.slope.value
        label = 'Slope = %.0f ks / s / Mpc' % slope_value if not isnan(slope_value) else None
        line = line_mark(layer, start_x, start_y, end_x, end_y, layer.state.color, label)


    def activate(self):
        self._fit_to_layers()

    def deactivate(self):
        pass

    def _fit_to_layers(self):
        for layer in self.viewer.layers:
            self._create_fit_line(layer)
            
            


    