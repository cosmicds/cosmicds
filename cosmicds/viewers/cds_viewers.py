# This file is for viewers that don't need anything beyond
# the standard CDS updating (the new toolbar, etc.)

from math import ceil, floor

from echo import add_callback, callback_property, CallbackProperty
from glue.config import viewer_tool
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.bqplot.histogram import BqplotHistogramView
from numpy import linspace, isnan

from cosmicds.components.toolbar import Toolbar
from cosmicds.utils import frexp10

def cds_viewer_state(state_class):

    class CDSViewerState(state_class):

        TICK_SPACINGS = [10, 7.5, 5, 4, 3, 2.5, 2, 1]

        xtick_values = CallbackProperty([])
        ytick_values = CallbackProperty([])

        @staticmethod
        def tick_spacing(naive_spacing):
            mantissa, exp = frexp10(naive_spacing)
            frac = CDSViewerState.best_spacing_frac(mantissa)
            return round(frac * (10 ** exp))

        @classmethod
        def best_spacing_frac(cls, frac):
            default = (-1, cls.TICK_SPACINGS[-1])
            index, fless = next(((i, t) for i, t in enumerate(cls.TICK_SPACINGS) if frac >= t), default)
            fmore = cls.TICK_SPACINGS[index - 1]
            dist_less = abs(frac - fless)
            dist_more = abs(frac - fmore)
            spacing = fless if dist_less < dist_more else fmore
            return spacing

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
            self.update_xticks(xmin=value)

        def _update_xmax(self, value):
            self.update_xticks(xmax=value)

        def _update_ymin(self, value):
            self.update_yticks(ymin=value)

        def _update_ymax(self, value):
            self.update_yticks(ymax=value)

        def update_xticks(self, xmin=None, xmax=None):
            xmin = xmin or self.x_min
            xmax = xmax or self.x_max
            if xmin is None or xmax is None:
                return
            x_range = xmax - xmin
            if isnan(x_range):
                x_range = 1
            naive = ceil(x_range / self.nxticks)
            spacing = CDSViewerState.tick_spacing(naive) if naive > 0 else 1
            self.set_xtick_spacing(spacing)

        def update_yticks(self, ymin=None, ymax=None):
            ymin = ymin or self.y_min
            ymax = ymax or self.y_max
            if ymin is None or ymax is None:
                return
            y_range = ymax - ymin
            if isnan(y_range):
                y_range = 1
            naive = ceil(y_range / self.nyticks)
            spacing = CDSViewerState.tick_spacing(naive) if naive > 0 else 1
            self.set_ytick_spacing(spacing)

        def set_xtick_spacing(self, spacing):
            xmin = 0 if isnan(self.x_min) else self.x_min
            xmax = 1 if isnan(self.x_max) else self.x_max
            tmin = ceil(xmin / spacing) * spacing
            tmax = floor(xmax / spacing) * spacing
            n = int(abs(tmax - tmin) / spacing) + 1
            self.xtick_values = list(linspace(tmin, tmax, n))

        def set_ytick_spacing(self, spacing):
            ymin = 0 if isnan(self.y_min) else self.y_min
            ymax = 1 if isnan(self.y_max) else self.y_max
            tmin = ceil(ymin / spacing) * spacing
            tmax = floor(ymax / spacing) * spacing
            n = int(abs(tmax - tmin) / spacing) + 1
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

        # The argument here can be either a Data or Subset object
        def layer_artist_for_data(self, data):
            return next((a for a in self.layers if a.layer == data), None)

        def _update_xtick_values(self, values):
            self.axis_x.tick_values = values
        
        def _update_ytick_values(self, values):
            self.axis_y.tick_values = values

    return CDSViewer


CDSScatterView = cds_viewer(
    BqplotScatterView,
    name='CDSScatterView',
    viewer_tools=[
        'cds:home',
        'bqplot:rectzoom',
        'bqplot:rectangle'
    ],
    label='2D scatter'
)

CDSHistogramView = cds_viewer(
    BqplotHistogramView,
    name='CDSHistogramView',
    viewer_tools=[
        'cds:home',
        'bqplot:xzoom',
        'bqplot:xrange'
    ],
    label='Histogram'
)
