from glue.config import viewer_tool
from glue.core import HubListener
from glue.core.message import (DataCollectionDeleteMessage, DataUpdateMessage,
                               LayerArtistUpdatedMessage, LayerArtistVisibilityMessage,
                               SubsetMessage, SubsetUpdateMessage)
from glue.core.exceptions import IncompatibleAttribute
from glue_jupyter.bqplot.common.tools import Tool
from numpy import isnan
from numpy.linalg import LinAlgError
from traitlets import Unicode, HasTraits
from cosmicds.message import CDSLayersUpdatedMessage

from cosmicds.utils import fit_line, line_mark

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
        self._show_labels = kwargs.get("show_labels", True)
        self._ignore_conditions = []
        self.hub.subscribe(self, DataCollectionDeleteMessage,
                           handler=self._on_data_collection_deleted, filter=self._data_collection_filter)
        self.hub.subscribe(self, DataUpdateMessage,
                           handler=self._on_data_updated, filter=self._data_update_filter)
        self.hub.subscribe(self, SubsetUpdateMessage,
                           handler=self._on_data_updated, filter=self._data_update_filter)
        self.hub.subscribe(self, LayerArtistVisibilityMessage,
                           handler=self._on_layer_visibility_updated, filter=self._layer_filter)
        self.hub.subscribe(self, CDSLayersUpdatedMessage,
                           handler=self._on_layers_updated, filter=self._layers_update_filter)
        self.hub.subscribe(self, LayerArtistUpdatedMessage, filter=self._layer_filter,
                           handler=self._on_layer_artist_updated)


    # Activation method

    def activate(self):
        if not self.active:
            self._fit_to_layers()
            self.tool_tip = self.active_tool_tip
        else:
            self._clear_lines()
            self.tool_tip = self.inactive_tool_tip
        self.active = not self.active


    # The label displayed for each line

    def label(self, layer, line):
        slope = line.slope.value
        return f"Slope: f{slope}" if not isnan(slope) else None


    # Message filters

    def _data_collection_filter(self, msg):
        return self.active and msg.data in self.lines.keys()

    def _create_filter(self, msg):
        return self.active and msg.subset.data in self.lines.keys()

    def _data_update_filter(self, msg):
        if not self.active:
            return False
        subset_message = isinstance(msg, SubsetMessage)
        subset = msg.subset if subset_message else None
        data = subset.data if subset_message else msg.data
        return (data in self.lines.keys() or subset in self.lines.keys()) \
            and msg.attribute in [self.viewer.state.x_att, self.viewer.state.y_att]

    def _layers_update_filter(self, msg):
        return self.active and msg.sender == self.viewer

    def _layer_filter(self, msg):
        return self.active and msg.layer_artist in self.viewer.layers


    # Message handlers

    def _on_data_collection_deleted(self, msg):
        remove = [layer for layer in self.lines.keys() if layer.state.layer == msg.data]
        lines = [self.lines[x] for x in remove]
        self.figure.marks = [mark for mark in self.figure.marks if mark not in lines]
        for layer in remove:
            self._remove_line(layer)

    def _refresh_if_active(self):
        if self.active:
            self._fit_to_layers()

    def _on_subset_created(self, msg):
        self._refresh_if_active()

    def _on_data_updated(self, msg):
        data = msg.subset if isinstance(msg, SubsetMessage) else msg.data
        self._update_fit_line_for_data(data)

    def _on_layers_updated(self, msg):
        self._refresh_if_active()

    def _on_layer_visibility_updated(self, msg):
        layer = msg.layer_artist
        visible = layer.state.visible
        if visible:
            self._update_fit_line(layer)
        else:
            self._remove_line(layer)

    def _on_layer_artist_updated(self, msg):
        layer = msg.layer_artist
        data = layer.state.layer
        mark = self.lines.get(data, None)
        if mark is None:
            return

        # Update the color
        # If we have other properties to update in the future, we can do so here
        color = layer.state.color if layer.state.color != '0.35' else 'black'
        if mark.colors[0] != color:
            mark.colors = [color]


    # Properties

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

    @property
    def line_marks(self):
        return self.lines.values()

    @property
    def x_range(self):
        return [0, 2 * self.viewer.state.x_max]

    @property
    def show_labels(self):
        return self._show_labels

    @show_labels.setter
    def show_labels(self, show):
        self._show_labels = show
        self._refresh_if_active()


    # Add or remove ignore conditions

    def add_ignore_condition(self, condition):
        self._ignore_conditions.append(condition)
        self._refresh_if_active()

    def remove_ignore_condition(self, condition):
        self._ignore_conditions.remove(condition)
        self._refresh_if_active()


    # Methods for fitting lines

    def _fit_line(self, layer):
        data = layer.state.layer
        x = data[self.viewer.state.x_att]
        y = data[self.viewer.state.y_att]
        return fit_line(x, y)

    def _create_fit_line(self, layer):

        # Do the fit
        fit = self._fit_line(layer)
        if fit is None:
            return None, None
    
        # Create the fit line object
        # Keep track of this line and its slope
        # For now, the line spans from 0 to twice the edge of the viewer
        y = fit(self.x_range)
        start_x, end_x = self.x_range
        start_y, end_y = y
        slope = fit.slope.value
        label = self.label(layer, fit) if self.show_labels else None
        color = layer.state.color if layer.state.color != '0.35' else 'black'
        line = line_mark(layer, start_x, start_y, end_x, end_y, color, label)
        return line, slope

    def _update_fit_line(self, layer):
        data = layer.state.layer
        if data in self.lines.keys():
            fit = self._fit_line(layer)
            if fit is None:
                return
            mark = self.lines[data]
            mark.x = self.x_range
            mark.y = fit(self.x_range)
            slope = fit.slope.value
            self.slopes[data] = slope
            label = self.label(layer, fit)
            is_label = label is not None
            mark.colors = [layer.state.color if layer.state.color != '0.35' else 'black']
            mark.display_legend = is_label
            mark.labels = [label] if is_label else []
        else:
            self._fit_to_layer(layer)


    def _fit_to_layer(self, layer, add_marks=True):
        try:
            line, slope = self._create_fit_line(layer)
            if line is None:
                return
            data = layer.state.layer
            self.lines[data] = line
            self.slopes[data] = slope
        except (IncompatibleAttribute, LinAlgError, SystemError) as e:
            pass

        if add_marks:
            self.figure.marks = self.figure.marks + [line]

    def _fit_to_layers(self):

        self._clear_lines()
        for layer in self.visible_layers:
            if not any(condition(layer) for condition in self._ignore_conditions):
                self._fit_to_layer(layer, add_marks=False)

        self.figure.marks = self.figure.marks + list(self.line_marks)

    def _update_fit_line_for_data(self, data):
        for layer in self.visible_layers:
            if layer.state.layer == data:
                self._update_fit_line(layer)
                return

    def _remove_line(self, layer):
        data = layer.state.layer
        line = self.lines.get(data, None)
        self.lines.pop(data, None)
        self.slopes.pop(data, None)
        self.figure.marks = [mark for mark in self.figure.marks if mark != line]

    def _clear_lines(self):
        self.figure.marks = [mark for mark in self.figure.marks if mark not in self.line_marks]
        self.lines = {}
        self.slopes = {}

    def refresh(self):
        self._refresh_if_active()
