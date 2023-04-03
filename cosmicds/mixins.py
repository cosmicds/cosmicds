from bqplot import Label
from bqplot.marks import Lines
from echo import CallbackProperty, add_callback, delay_callback
from ipyvuetify import VuetifyTemplate
from glue.config import viewer_tool
from glue.core import HubListener
from glue.viewers.common.utils import get_viewer_tools

from cosmicds.components.toolbar import Toolbar

__all__ = ['HubMixin', 'TemplateMixin']


class HubMixin(HubListener):
    @property
    def app(self):
        return self._session.application

    @property
    def hub(self):
        return self._session.hub

    @property
    def session(self):
        return self._session

    @property
    def data_collection(self):
        return self._session.data_collection


class TemplateMixin(VuetifyTemplate, HubMixin):
    pass


class LineHoverStateMixin:
    _YMAX_FACTOR = 1.5

    resolution_x = CallbackProperty(0)
    resolution_y = CallbackProperty(0)

    show_line = CallbackProperty(True)
    show_previous = CallbackProperty(True)
    show_label = CallbackProperty(True)
    show_previous_label = CallbackProperty(True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def ymax_factor(self):
        return self._YMAX_FACTOR
    
    def reset_limits(self):
        with delay_callback(self, 'x_min', 'x_max', 'y_min', 'y_max'):
            xmin, xmax = self.x_min, self.x_max
            ymin, ymax = self.y_min, self.y_max
            super().reset_limits()
            self.y_max = self._YMAX_FACTOR * self.y_max
            self.resolution_x *= (self.x_max - self.x_min) / (xmax - xmin)
            self.resolution_y *= (self.y_max - self.y_min) / (ymax - ymin)

class LineHoverViewerMixin:

    _x_zoom_id = None

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.figure_size_x = 0
        self.figure_size_y = 230
        self._resolution_dirty = True

        self.line = Lines(
            x=[0, 0],
            y=[0, 0],
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            colors=['#1b3e6a'],
        )

        self.line_label = Label(
            text=[""],
            x=[],
            y=[],
            x_offset=10,
            y_offset=10,
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            colors=['#1b3e6a'],
        )

        self.label_background = Lines(
            x=[0, 0],
            y=[0, 0],
            stroke_width=25,
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            colors=['white'],
            opacities=[0.8]
        )

        self.previous_line = Lines(
            x=[0, 0],
            y=[0, 0],
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            },
            colors=['#a7a5a5'],
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
            colors=['#747272'],
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
            opacities=[0.8]
        )

        self.figure.marks += [
            self.previous_label_background,
            self.previous_line, self.previous_line_label,
            self.label_background, self.line,
            self.line_label,
        ]

        add_callback(self.state, 'show_line', self._show_line_changed)
        add_callback(self.state, 'show_previous', self._show_previous_changed)
        add_callback(self.state, 'show_label', self._show_label_changed)
        add_callback(self.state, 'show_previous_label', self._show_previous_label_changed)

        self.scale_y.observe(self._update_locations, names=['min', 'max'])
        add_callback(self.state, 'x_min', self._on_xmin_change, echo_old=True)
        add_callback(self.state, 'x_max', self._on_xmax_change, echo_old=True)
        add_callback(self.state, 'y_min', self._on_ymin_change, echo_old=True)
        add_callback(self.state, 'y_max', self._on_ymax_change, echo_old=True)
        add_callback(self.state, 'resolution_x', self._update_x_locations)
        add_callback(self.state, 'resolution_y', self._update_y_locations)

    def _show_line_changed(self, show):
        self.line.visible = show
        show_label = show and self.show_label
        self.line_label.visible = show_label
        self.label_background.visible = show_label

    def _show_previous_changed(self, show):
        self.previous_line.visible = show
        show_label = show and self.show_previous_label
        self.previous_line_label.visible = show_label
        self.previous_label_background.visible = show_label

    def _show_label_changed(self, show):
        show_label = self.show_line and show
        self.line_label.visible = show_label
        self.label_background.visible = show_label

    def _show_previous_label_changed(self, show):
        show_label = self.show_previous and show
        self.previous_line_label.visible = show_label
        self.previous_label_background.visible = show_label

    def _x_background_coordinates(self, x):
        return [x + 10 * self.state.resolution_x,
                x + 65 * self.state.resolution_x]

    def _y_background_coordinates(self, y):
        return [y - 10 * self.state.resolution_y,
                y - 10 * self.state.resolution_y]
    
    def _update_x_locations(self, resolution=None):
        self.line_label.x = [self.line.x[0]]
        self.label_background.x = self._x_background_coordinates(
            self.line_label.x[0])
        self.previous_line_label.x = [self.previous_line.x[0]]
        self.previous_label_background.x = self._x_background_coordinates(
            self.previous_line_label.x[0])

    def _update_y_locations(self, resolution=None):
        scale = self.scales['y']
        ymin, ymax = scale.min, scale.max

        if ymin is None or ymax is None:
            return
        
        line_bounds = [ymin, ymax / self.state.ymax_factor]
        
        self.line.y = line_bounds
        self.previous_line.y = line_bounds
        self.line_label.y = [self.line.y[1]]
        self.label_background.y = self._y_background_coordinates(
            self.line_label.y[0])
        self.previous_line_label.y = [self.previous_line.y[1]]
        self.previous_label_background.y = self._y_background_coordinates(
            self.previous_line_label.y[0])

    def _update_locations(self, event=None):
        self._update_x_locations()
        self._update_y_locations()

    def _on_xmin_change(self, old, new):
        if old is not None:
            xmax = self.state.x_max
            self.state.resolution_x *= (xmax - new) / (xmax - old)
        self._update_x_locations()

    def _on_xmax_change(self, old, new):
        if old is not None:
            xmin = self.state.x_min
            self.state.resolution_x *= (new - xmin) / (old - xmin)
        self._update_x_locations()

    def _on_ymin_change(self, old, new):
        if old is not None:
            ymax = self.state.y_max
            self.state.resolution_y *= (ymax - new + 20) / (ymax - old + 20)
        self._update_y_locations()

    def _on_ymax_change(self, old, new):
        if old is not None:
            ymin = self.state.y_min
            self.state.resolution_y *= (new - ymin + 20) / (old - ymin + 20)
        self._update_y_locations()

    @staticmethod
    def _label_text(value):
        return f"{value:.0f}"

    def _on_mouse_moved(self, event):

        if not self.line.visible \
                or self.state.x_min is None:
            return

        new_x = event['domain']['x']

        if self._resolution_dirty:
            pixel_x = event['pixel']['x']
            y = event['domain']['y']
            pixel_y = event['pixel']['y']
            self.state.resolution_x = (new_x - self.state.x_min) / pixel_x
            if self.state.resolution_x != 0:
                self.figure_size_x = (self.state.x_max - self.state.x_min) / self.state.resolution_x
            self.state.resolution_y = (self.state.y_max - y) / (
                        pixel_y - 10)  # The y-axis has 10px "extra" on the top and bottom
            if self.state.resolution_y != 0:
                self.figure_size_y = (self.state.y_max - self.state.y_min) / self.state.resolution_y
            self._resolution_dirty = False

        self.line_label.text = [self._label_text(new_x)]
        self.line.x = [new_x, new_x]
        self.line_label.x = [new_x, new_x]
        self.label_background.x = self._x_background_coordinates(self.line_label.x[0])
        self.label_background.y = self._y_background_coordinates(self.line_label.y[0])

    def _on_click(self, event):
        new_x = event['domain']['x']
        self.previous_line.x = [new_x, new_x]
        self.previous_line_label.text = [self._label_text(new_x)]
        self.previous_line_label.x = [new_x, new_x]
        self.previous_label_background.x = self._x_background_coordinates(
            new_x)
        self.previous_label_background.y = self._y_background_coordinates(
            self.previous_line_label.y[0])
        self.previous_line.visible = True
        self.previous_line_label.visible = True
        self.previous_label_background.visible = True
