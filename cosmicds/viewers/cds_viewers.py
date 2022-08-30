# This file is for viewers that don't need anything beyond
# the standard CDS updating (the new toolbar, etc.)

from math import ceil, floor

from echo import add_callback, callback_property, CallbackProperty
from glue.config import viewer_tool
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.bqplot.histogram import BqplotHistogramView
from numpy import linspace

from cosmicds.components.toolbar import Toolbar

def cds_viewer_state(state_class):

    class CDSViewerState(state_class):

        TICK_SPACINGS = tick_spacings = [2000, 1500, 1000, 500, 250, 200, 100, 75, 50, 25, 10, 5, 2, 1, 0.75, 0.5, 0.2, 0.1]

        xtick_values = CallbackProperty([])
        ytick_values = CallbackProperty([])

        @callback_property
        def nxticks(self):
            return self._nxticks

        @nxticks.setter
        def nxticks(self, nticks):
            if nticks == self._nxticks:
                return
            self._nxticks = max(nticks, 1)
            self.update_xticks()

        @callback_property
        def nyticks(self):
            return self._nyticks

        @nyticks.setter
        def nyticks(self, nticks):
            if nticks == self._nyticks:
                return
            self._nyticks = max(nticks, 1)
            self.update_yticks()

        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._nxticks = 7
            self._nyticks = 7
            add_callback(self, "x_min", self._update_xmin)
            add_callback(self, "x_max", self._update_xmax)
            add_callback(self, "y_min", self._update_ymin)
            add_callback(self, "y_max", self._update_ymax)

        def _update_xmin(self, value):
            self.update_xticks(min=value)

        def _update_xmax(self, value):
            self.update_xticks(max=value)

        def _update_ymin(self, value):
            self.update_yticks(min=value)

        def _update_ymax(self, value):
            self.update_yticks(max=value)

        def update_xticks(self, min=None, max=None):
            min = min or self.x_min
            max = max or self.x_max
            if min is None or max is None:
                return
            x_range = max - min
            frac = int(x_range / self.nxticks)
            spacing = next((t for t in self.TICK_SPACINGS if frac > t), self.TICK_SPACINGS[-1])
            self.set_xtick_spacing(spacing)

        def update_yticks(self, min=None, max=None):
            min = min or self.y_min
            max = max or self.y_max
            if min is None or max is None:
                return
            y_range = max - min
            frac = int(y_range / self.nyticks)
            spacing = next((t for t in self.TICK_SPACINGS if frac > t), self.TICK_SPACINGS[-1])
            self.set_ytick_spacing(spacing)

        def set_xtick_spacing(self, spacing):
            tmin = ceil(self.x_min / spacing) * spacing
            tmax = floor(self.x_max / spacing) * spacing
            n = int((tmax - tmin) / spacing) + 1
            self.xtick_values = list(linspace(tmin, tmax, n))

        def set_ytick_spacing(self, spacing):
            tmin = ceil(self.y_min / spacing) * spacing
            tmax = floor(self.y_max / spacing) * spacing
            n = int((tmax - tmin) / spacing) + 1
            self.ytick_values = list(linspace(tmin, tmax, n))

    return CDSViewerState


def cds_viewer(viewer_class, name, viewer_tools=[], label=None, state_cls=None):

    state_class = state_cls or viewer_class._state_cls
    cds_state_class = cds_viewer_state(state_class)

    class CDSViewer(viewer_class):

        __name__ = name
        __qualname__ = name
        _state_cls = cds_state_class
        inherit_tools = viewer_tools is None
        tools = viewer_tools or viewer_class.tools
        LABEL = label or viewer_class.LABEL

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ignore_conditions = []
            add_callback(self.state, "xtick_values", self._update_xtick_values)
            add_callback(self.state, "ytick_values", self._update_ytick_values)

        def initialize_toolbar(self):
            self.toolbar = Toolbar(self)

            for tool_id in self.tools:
                mode_cls = viewer_tool.members[tool_id]
                mode = mode_cls(self)
                self.toolbar.add_tool(mode)

        def ignore(self, condition):
            self.ignore_conditions.append(condition)

        def add_data(self, data):
            if any(condition(data) for condition in self.ignore_conditions):
                return False
            return super().add_data(data)

        def add_subset(self, subset):
            if any(condition(subset) for condition in self.ignore_conditions):
                return False
            return super().add_subset(subset)

        def _update_xtick_values(self, values):
            self.axis_x.tick_values = values
        
        def _update_ytick_values(self, values):
            self.axis_y.tick_values = values

        
    return CDSViewer


CDSScatterView = cds_viewer(
    BqplotScatterView,
    name='CDSScatterView',
    viewer_tools=[
        'bqplot:home',
        'bqplot:rectzoom',
        'bqplot:rectangle'
    ],
    label='2D scatter'
)

CDSHistogramView = cds_viewer(
    BqplotHistogramView,
    name='CDSHistogramView',
    viewer_tools=[
        'bqplot:home',
        'bqplot:xzoom',
        'bqplot:xrange'
    ],
    label='Histogram'
)
