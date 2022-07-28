from glue.viewers.scatter.state import ScatterViewerState
from glue_jupyter.bqplot.scatter import BqplotScatterView, BqplotScatterLayerArtist
from bqplot.marks import Lines
from bqplot import Label
from echo import add_callback, delay_callback
from glue.config import viewer_tool
from glue.viewers.common.utils import get_viewer_tools
from traitlets import Bool

from cosmicds.components.toolbar import Toolbar
from cosmicds.stories.hubbles_law.utils import H_ALPHA_REST_LAMBDA, MG_REST_LAMBDA

__all__ = ['SpectrumView', 'SpectrumViewLayerArtist', 'SpectrumViewerState']


class SpectrumViewerState(ScatterViewerState):

    _YMAX_FACTOR = 1.5

    @property
    def ymax_factor(self):
        return self._YMAX_FACTOR

    def reset_limits(self):
        with delay_callback(self, 'x_min', 'x_max', 'y_min', 'y_max'):
            super().reset_limits()
            self.y_max = self._YMAX_FACTOR * self.y_max


class SpectrumViewLayerArtist(BqplotScatterLayerArtist):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        old_scatter = self.scatter
        self.scatter = Lines(scales=self.scales, x=[0,1], y=[0,1], marker=None)
        self.view.figure.marks = list(filter(lambda x: x is not old_scatter, self.view.figure.marks)) + [self.scatter]
        
class SpectrumView(BqplotScatterView):

    _data_artist_cls = SpectrumViewLayerArtist
    _subset_artist_cls = SpectrumViewLayerArtist

    inherit_tools = False
    tools = ['bqplot:home', 'hubble:wavezoom', 'hubble:restwave', 'hubble:specflag', 'cds:info']
    _state_cls = SpectrumViewerState
    show_line = Bool(True)
    LABEL = "Spectrum Viewer"

    observed_text = ' (observed)'
    rest_text = ' (rest)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.resolution_x = 0
        self.resolution_y = 0
        self.element = None
        
        self.user_line = Lines(
            x=[0, 0], 
            y=[0, 0], 
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            })

        self.label_background = Lines(
            x=[0, 0],
            y=[0, 0],
            stroke_width=25,
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            colors=['white'],
            opacities=[0.7]
        )
        
        self.user_line_label = Label(
            text=[""], 
            x=[], 
            y=[],
            x_offset=10,
            y_offset=10,
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            })

        self.previous_line = Lines(
            x=[0, 0],
            y=[0, 0],
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            colors=['gray'],
            visible=False
        )

        self.previous_line_label = Label(
            text=[""], 
            x=[], 
            y=[],
            x_offset=10,
            y_offset=10,
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            colors=['gray'],
            visible=False
        )

        self.previous_label_background = Lines(
            x=[0, 0],
            y=[0, 0],
            stroke_width=25,
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            colors=['white'],
            opacities=[0.7]
        )

        self.element_tick = Lines(
            x=[],
            y=[0, 0],
            x_offset=-10,
            opacities=[0.7],
            colors=['red'],
            stroke_width=10,
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            })

        self.element_label = Label(
            text=["H-α"],
            x=[],
            y=[],
            x_offset=-5,
            opacities=[0.7],
            colors=['red'],
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            })
        
        self.figure.marks += [self.previous_label_background, self.previous_line, self.previous_line_label,
                              self.label_background, self.user_line, self.user_line_label,
                              self.element_tick, self.element_label]
        
        self.add_event_callback(self._on_mouse_moved, events=['mousemove'])
        self.add_event_callback(self._on_click, events=['click'])
        self.scale_y.observe(self._on_view_change, names=['min', 'max'])

        add_callback(self.state, 'y_min', self._on_view_change)
        add_callback(self.state, 'y_max', self._on_view_change)
        self.toolbar.observe(self._active_tool_change, names=['active_tool'])

    @staticmethod
    def _label_text(value):
        return f"{value:.0f} Å"

    def _x_background_coordinates(self, x):
        return [x + 10 * self.resolution_x, x + 65 * self.resolution_x]

    def _y_background_coordinates(self, y):
        return [y - 10 * self.resolution_y, y - 10 * self.resolution_y]

    def _active_tool_change(self, change):
        is_tool = change.new is not None
        line_visible = not is_tool or change.new.tool_id != 'hubble:wavezoom'
        self.user_line.visible = line_visible
        self.user_line_label.visible = line_visible

    def _on_view_change(self, event=None):
        scale = self.scales['y']
        ymin, ymax = scale.min, scale.max
        
        if ymin is None or ymax is None:
            return
        
        line_bounds = [ymin, ymax / self.state.ymax_factor]
        tick_bounds = [ymax * 0.74, ymax * 0.87]
        bottom_label_position = ymax * 0.91
        self.user_line.y = line_bounds
        self.previous_line.y = line_bounds
        self.user_line_label.x = [self.user_line.x[0]]
        self.user_line_label.y = [self.user_line.y[1]]
        self.label_background.x = self._x_background_coordinates(self.user_line_label.x[0])
        self.label_background.y = self._y_background_coordinates(self.user_line_label.y[0])
        self.previous_line_label.x = [self.previous_line.x[0]]
        self.previous_line_label.y = [self.previous_line.y[1]]
        self.previous_label_background.x = self._x_background_coordinates(self.previous_line_label.x[0])
        self.previous_label_background.y = self._y_background_coordinates(self.previous_line_label.y[0])
        self.element_tick.y = tick_bounds
        self.element_label.y = [bottom_label_position]
  
    def _on_mouse_moved(self, event):

        if not self.user_line.visible \
            or self.state.x_min is None:
            return

        new_x = event['domain']['x']
        pixel_x = event['pixel']['x']
        y = event['domain']['y']
        pixel_y = event['pixel']['y']
        self.resolution_x = (new_x - self.state.x_min) / pixel_x
        self.resolution_y = (self.state.y_max - y) / (pixel_y - 10) # The y-axis has 10px "extra" on the top and bottom
        self.user_line_label.text = [self._label_text(new_x)]
        self.user_line.x = [new_x, new_x]
        self.user_line_label.x = [new_x, new_x]
        self.label_background.x = self._x_background_coordinates(self.user_line_label.x[0])
        self.label_background.y = self._y_background_coordinates(self.user_line_label.y[0])

    def _on_click(self, event):
        new_x = event['domain']['x']
        self.previous_line.x = [new_x, new_x]
        self.previous_line_label.text = [self._label_text(new_x)]
        self.previous_line_label.x = [new_x, new_x]
        self.previous_label_background.x = self._x_background_coordinates(new_x)
        self.previous_label_background.y = self._y_background_coordinates(self.previous_line_label.y[0])
        self.previous_line.visible = True
        self.previous_line_label.visible = True

    def update(self, name, element, z, previous=None):
        self.spectrum_name = name
        self.element = element
        self.z = z
        rest = MG_REST_LAMBDA if element == 'Mg-I' else H_ALPHA_REST_LAMBDA
        self.shifted = rest * (1 + z)
        items_visible = bool(z > 0) # The bqplot Mark complained without the explicit bool() call
        self.element_label.visible = items_visible
        self.element_tick.visible = items_visible
        self.user_line.visible = items_visible
        self.user_line_label.visible = items_visible
        self.label_background.visible = items_visible
        has_previous = previous is not None
        self.previous_line.visible = has_previous
        self.previous_line_label.visible = has_previous
        if has_previous:
            self.previous_line.x = [previous, previous]
            self.previous_line_label.x = [previous, previous]
            self.previous_line_label.text = [self._label_text(previous)]
            self.previous_label_background.x = self._x_background_coordinates(previous)
        self.element_label.x = [self.shifted, self.shifted]
        self.element_label.text = [element]
        self.element_tick.x = [self.shifted, self.shifted]
        self._on_view_change()

    def add_data(self, data):
        super().add_data(data)
        self.state.x_att = data.id['lambda']
        self.state.y_att = data.id['flux']
        self.layers[0].state.attribute = data.id['flux']
        for layer in self.layers:
            if layer.state.layer.label != data.label:
                layer.state.visible = False

        bring_to_front = [
            self.previous_label_background, self.previous_line, self.previous_line_label,
            self.label_background, self.user_line, self.user_line_label
        ]
        marks = [x for x in self.figure.marks if x not in bring_to_front]
        self.figure.marks = marks + bring_to_front

    def initialize_toolbar(self):
        self.toolbar = Toolbar(self)

        tool_ids, subtool_ids = get_viewer_tools(self.__class__)

        if subtool_ids:
            raise ValueError('subtools are not yet supported in Jupyter viewers')

        for tool_id in tool_ids:
            mode_cls = viewer_tool.members[tool_id]
            mode = mode_cls(self)
            self.toolbar.add_tool(mode)

    @property
    def line_visible(self):
        return self.user_line.visible
