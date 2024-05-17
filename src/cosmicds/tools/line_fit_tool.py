from echo import add_callback
from glue.config import viewer_tool
from glue.core import HubListener
from glue.core.message import (DataCollectionDeleteMessage, DataUpdateMessage,
                               LayerArtistUpdatedMessage, LayerArtistVisibilityMessage,
                               NumericalDataChangedMessage,
                               SubsetMessage, SubsetUpdateMessage)
from glue.core.exceptions import IncompatibleAttribute
from glue_jupyter.bqplot.common.tools import Tool
from numpy import isnan
from numpy.linalg import LinAlgError
from traitlets import Unicode, HasTraits

from . import register_tool
from cosmicds.utils import fit_line, line_mark



@register_tool
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
        self.hub.subscribe(self, LayerArtistUpdatedMessage, filter=self._layer_filter,
                           handler=self._on_layer_artist_updated)
        self.hub.subscribe(self, NumericalDataChangedMessage, filter=self._data_collection_filter,
                           handler=self._on_data_updated)

        add_callback(self.viewer.state, 'layers', self._on_layers_updated)


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
        return f"Slope: {slope}" if not isnan(slope) else None


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

    def _layer_filter(self, msg):
        return self.active and msg.layer_artist in self.viewer.layers


    # Message handlers

    def _on_data_collection_deleted(self, msg):
        remove = [data for data in self.lines.keys() if data == msg.data]
        lines = [self.lines[x] for x in remove]
        self.figure.data = [mark for mark in self.figure.data if mark not in lines]
        for state in remove:
            self._remove_line(state)

    def _refresh_if_active(self):
        if self.active:
            self._fit_to_layers()

    def _on_subset_created(self, msg):
        self._refresh_if_active()

    def _on_data_updated(self, msg):
        data = msg.subset if isinstance(msg, SubsetMessage) else msg.data
        self._update_fit_line_for_data(data)

    def _on_layers_updated(self, layers):
        self._refresh_if_active()

    def _on_layer_visibility_updated(self, msg):
        layer = msg.layer_artist
        state = layer.state
        visible = state.visible
        if visible:
            self._update_fit_line(state)
        else:
            self._remove_line(state)

    def _on_layer_artist_updated(self, msg):
        layer = msg.layer_artist
        data = layer.state.layer
        mark = self.lines.get(data, None)
        if mark is None:
            return

        # Update the color
        # If we have other properties to update in the future, we can do so here
        color = self._get_layer_color(layer.state)
        if mark.color != color:
            mark.color = color


    # Properties

    @property
    def figure(self):
        return self.viewer.figure

    @property
    def dc(self):
        return self.viewer.session.data_collection

    @property
    def visible_layers(self):
        return filter(lambda state: state.visible, self.viewer.state.layers)

    @property
    def layer_labels(self):
        return [state.layer.label for state in self.viewer.state.layers]

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
        if show != self._show_labels:
            self._show_labels = show
            self._refresh_if_active()


    # Add or remove ignore conditions

    def add_ignore_condition(self, condition):
        self._ignore_conditions.append(condition)
        self._refresh_if_active()

    def remove_ignore_condition(self, condition):
        self._ignore_conditions.remove(condition)
        self._refresh_if_active()
    
    @staticmethod
    def _get_layer_color(state):
        color = state.color if state.color != '0.35' else 'black'
        try:
            # convert to hex for Plotly
            color = float(color)
            h = f"{int(color * 255):02x}"
            color = f"#{h}{h}{h}"
        except ValueError:
            pass
        return color


    # Methods for fitting lines

    def _fit_line(self, state):
        data = state.layer
        x = data[self.viewer.state.x_att]
        y = data[self.viewer.state.y_att]
        return fit_line(x, y)

    def _create_fit_line(self, state):

        # Do the fit
        fit = self._fit_line(state)
        if fit is None:
            return None, None
    
        # Create the fit line object
        # Keep track of this line and its slope
        # For now, the line spans from 0 to twice the edge of the viewer
        y = fit(self.x_range)
        start_x, end_x = self.x_range
        start_y, end_y = y
        slope = fit.slope.value
        label = self.label(state, fit) if self.show_labels else None
        color = self._get_layer_color(state)
        line = line_mark(start_x, start_y, end_x, end_y, color, label)
        return line, slope

    def _update_fit_line(self, state):
        data = state.layer
        if data in self.lines.keys():
            fit = self._fit_line(state)
            if fit is None:
                return
            mark = self.lines[data]
            mark.x = self.x_range
            mark.y = fit(self.x_range)
            slope = fit.slope.value
            self.slopes[data] = slope
            label = self.label(state, fit) if self.show_labels else None
            is_label = label is not None
            mark.marker['color'] = self._get_layer_color(state)
            mark.showlegend = is_label
            mark.name = label if is_label else ''
        else:
            self._fit_to_layer(state)


    def _fit_to_layer(self, state, add_marks=True):
        try:
            line, slope = self._create_fit_line(state)
            if line is None:
                return
            data = state.layer
            if add_marks:
                line = self.figure.add_trace(line).data[-1]
            self.lines[data] = line
            self.slopes[data] = slope
        except (IncompatibleAttribute, LinAlgError, SystemError) as e:
            pass

        

    def _fit_to_layers(self):
        self._clear_lines()
        for state in self.visible_layers:
            if not any(condition(state) for condition in self._ignore_conditions):
                self._fit_to_layer(state, add_marks=True)

    def _update_fit_line_for_data(self, data):
        for state in self.visible_layers:
            if state.layer == data:
                self._update_fit_line(state)
                return

    def _remove_line(self, state):
        data = state.layer
        line = self.lines.get(data, None)
        self.lines.pop(data, None)
        self.slopes.pop(data, None)
        self.figure.data = [mark for mark in self.figure.data if mark != line]

    def _clear_lines(self):
        self.figure.data = [mark for mark in self.figure.data if mark not in self.line_marks]
        self.lines = {}
        self.slopes = {}

    def refresh(self):
        self._refresh_if_active()
