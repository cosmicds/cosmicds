from glue.core.message import NumericalDataChangedMessage
from glue.viewers.scatter.state import ScatterViewerState
from glue_jupyter.bqplot.scatter import BqplotScatterView
from bqplot.marks import Lines
from bqplot import Label
from echo import add_callback, delay_callback
from glue.config import viewer_tool
from glue.viewers.common.utils import get_viewer_tools
from traitlets import Bool
from cosmicds.components.toolbar import Toolbar
from cosmicds.stories.hubbles_law.utils import H_ALPHA_REST_LAMBDA, MG_REST_LAMBDA

# We need to import this so that it gets loaded into the registry first
from cosmicds.tools import BqplotXZoom
from cosmicds.utils import extend_tool

__all__ = ['SpectrumView', 'SpectrumViewerState']


class SpectrumViewerState(ScatterViewerState):

    def reset_limits(self):
        with delay_callback(self, 'y_min', 'y_max'):
            super().reset_limits()
            self.y_max = 1.40 * self.y_max

class SpectrumView(BqplotScatterView):

    inherit_tools = False
    tools = ['bqplot:home', 'bqplot:xzoom']
    _state_cls = SpectrumViewerState
    show_line = Bool(True)
    LABEL = "Spectrum Viewer"

    observed_text = ' (observed)'
    rest_text = ' (rest)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.h_alpha_shifted = None
        self.mg_shifted = None
        self.observed_label = None
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

        self.h_alpha_tick = Lines(
            x=[H_ALPHA_REST_LAMBDA, H_ALPHA_REST_LAMBDA],
            y=[0, 0],
            x_offset=-10,
            opacities=[0.7],
            colors=['red'],
            stroke_width=10,
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            visible=False)

        self.h_alpha_label = Label(
            text=["H-α"],
            x=[H_ALPHA_REST_LAMBDA],
            y=[],
            x_offset=-5,
            opacities=[0.7],
            colors=['red'],
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            visible=False)

        self.mg_tick = Lines(
            x=[MG_REST_LAMBDA, MG_REST_LAMBDA],
            y=[0, 0],
            x_offset=-10,
            opacities=[0.7],
            colors=['green'],
            stroke_width=10,
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            visible=False)

        self.mg_label = Label(
            text=["Mg-I"],
            x=[MG_REST_LAMBDA],
            y=[],
            x_offset=-5,
            opacities=[0.7],
            colors=['green'],
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            visible=False)

        self.visible_wavelength_line = Lines(
            x=[0, 0],
            y=[0, 0],
            line_style='dotted',
            opacities=[0.7],
            colors=['black'],
            scales={
                'x': self.scales['x'],
                'y': self.scales['y']
            },
            visible=False
        )

        self.visible_wavelength_label = Label(
            text=[""],
            x=[],
            y=[],
            x_offset=-5,
            opacities=[0.7],
            colors=['black'],
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            visible=False
        )
        
        self.figure.marks += [self.user_line, self.user_line_label,
                              self.h_alpha_tick, self.h_alpha_label,
                              self.mg_tick, self.mg_label,
                              self.visible_wavelength_line, self.visible_wavelength_label]
        
        self.add_event_callback(self._on_mouse_moved, events=['mousemove'])
        self.scale_y.observe(self._on_view_change, names=['min', 'max'])

        add_callback(self.state, 'y_min', self._on_view_change)
        add_callback(self.state, 'y_max', self._on_view_change)

        def zoom_activate():
            self.user_line.visible = False
            self.user_line_label.visible = False
        def zoom_deactivate():
            self.user_line.visible = True
            self.user_line_label.visible = True
        extend_tool(self, 'bqplot:xzoom', zoom_activate, zoom_deactivate)

    def _on_view_change(self, event=None):
        scales = self.scales['y']
        
        if scales.min is None or scales.max is None:
            return
        
        ymin, ymax = self.scales['y'].min, self.scales['y'].max
        line_bounds = [ymin, ymax / 1.4]
        tick_bounds = [ymax * 0.78, ymax * 0.83]
        bottom_label_position = ymax * 0.88
        top_label_position = ymax * 0.96
        restwave_line_bounds = [ymin, ymax * 0.93]
        self.user_line.y = line_bounds
        self.user_line_label.x = [self.user_line.x[0]]
        self.user_line_label.y = [self.user_line.y[1]]
        self.h_alpha_tick.y = tick_bounds
        self.h_alpha_label.y = [bottom_label_position]
        self.mg_tick.y = tick_bounds
        self.mg_label.y = [bottom_label_position]
        self.visible_wavelength_label.y = [top_label_position]
        self.visible_wavelength_line.y = restwave_line_bounds
        
    def _on_mouse_moved(self, event):

        if not self.user_line.visible:
            return

        new_x = event['domain']['x']
        pixel_x = event['pixel']['x']
        self.resolution = (new_x - self.state.x_min) / pixel_x
        self.user_line_label.text = [f"{new_x:.0f}"]

        self.user_line.x = [new_x, new_x]
        self.user_line_label.x = [new_x, new_x]

    def update_element(self, element):
        self.element = element
        use_mg = element == 'Mg-I'
        self.h_alpha_tick.visible = not use_mg
        self.h_alpha_label.visible = not use_mg
        self.mg_label.visible = use_mg
        self.mg_tick.visible = use_mg

    def update_z(self, z):
        self.z = z
        self.h_alpha_shifted = H_ALPHA_REST_LAMBDA * (1 + z)
        self.mg_shifted = MG_REST_LAMBDA * (1 + z)
        self.h_alpha_tick.x = [self.h_alpha_shifted, self.h_alpha_shifted]
        self.h_alpha_label.x = [self.h_alpha_shifted]
        self.mg_tick.x = [self.mg_shifted, self.mg_shifted]
        self.mg_label.x = [self.mg_shifted]

    def update(self, element, z):
        self.element = element
        self.z = z
        self.hide_rest_wavelength()

    def add_data(self, data):
        super().add_data(data)
        self.state.x_att = data.id['lambda']
        self.state.y_att = data.id['flux']
        self.layers[0].state.attribute = data.id['flux']
        for layer in self.layers:
            if layer.state.layer.label != data.label:
                layer.state.visible = False

    def show_rest_wavelength(self):
        use_mg = self.element == 'Mg-I'
        lambda_rest = MG_REST_LAMBDA if use_mg else H_ALPHA_REST_LAMBDA
        self.visible_wavelength_label.text = [self.element + self.rest_text]
        self.visible_wavelength_line.x = [lambda_rest, lambda_rest]
        self.visible_wavelength_label.x = [lambda_rest, lambda_rest]
        self.visible_wavelength_line.visible = True
        self.visible_wavelength_label.visible = True

        self.observed_label = self.mg_label if use_mg else self.h_alpha_label
        self.observed_label.text = [self.observed_label.text[0] + self.observed_text]

    def hide_rest_wavelength(self):
        self.visible_wavelength_line.visible = False
        self.visible_wavelength_label.visible = False
        if self.observed_label is not None:
            self.observed_label.text = [self.observed_label.text[0][:-len(self.observed_text)]]

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
    def rest_wavelength_shown(self):
        return self.visible_wavelength_line.visible

