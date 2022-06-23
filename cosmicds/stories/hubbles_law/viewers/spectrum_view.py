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

    def reset_limits(self):
        with delay_callback(self, 'x_min', 'x_max', 'y_min', 'y_max'):
            super().reset_limits()
            self.y_max = 1.40 * self.y_max


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

        self.resolution = 0
        self.element = None
        
        self.user_line = Lines(
            x=[0, 0], 
            y=[0, 0], 
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            })
        
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
        
        self.figure.marks += [self.user_line, self.user_line_label,
                              self.element_tick, self.element_label]
        
        self.add_event_callback(self._on_mouse_moved, events=['mousemove'])
        self.scale_y.observe(self._on_view_change, names=['min', 'max'])

        add_callback(self.state, 'y_min', self._on_view_change)
        add_callback(self.state, 'y_max', self._on_view_change)
        self.toolbar.observe(self._active_tool_change, names=['active_tool'])

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
        
        line_bounds = [ymin, ymax / 1.4]
        tick_bounds = [ymax * 0.78, ymax * 0.83]
        bottom_label_position = ymax * 0.88
        self.user_line.y = line_bounds
        self.user_line_label.x = [self.user_line.x[0]]
        self.user_line_label.y = [self.user_line.y[1]]
        self.element_tick.y = tick_bounds
        self.element_label.y = [bottom_label_position]
  
    def _on_mouse_moved(self, event):

        if not self.user_line.visible:
            return

        new_x = event['domain']['x']
        pixel_x = event['pixel']['x']
        self.resolution = (new_x - self.state.x_min) / pixel_x
        self.user_line_label.text = [f"{new_x:.0f} Å"]

        self.user_line.x = [new_x, new_x]
        self.user_line_label.x = [new_x, new_x]

    def update(self, name, element, z):
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
