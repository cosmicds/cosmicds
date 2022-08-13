# This file is for viewers that don't need anything beyond
# the standard CDS updating (the new toolbar, etc.)

from math import ceil, floor

from glue.config import viewer_tool
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.bqplot.histogram import BqplotHistogramView
from numpy import linspace

from cosmicds.components.toolbar import Toolbar


def cds_viewer(viewer_class, name=None, viewer_tools=None, label=None, state_cls=None):
    class CDSViewer(viewer_class):

        __name__ = name
        __qualname__ = name
        _state_cls = state_cls or viewer_class._state_cls
        inherit_tools = viewer_tools is None
        tools = viewer_tools or viewer_class.tools
        LABEL = label or viewer_class.LABEL

        TICK_SPACINGS = tick_spacings = [2000, 1500, 1000, 500, 250, 200, 100, 75, 50, 25, 10, 5, 2, 1, 0.75, 0.5, 0.2, 0.1]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ignore_conditions = []
            self.nxticks = 7
            self.nyticks = 7
            self.scale_x.observe(self._on_xaxis_change, names=['min', 'max'])
            self.scale_y.observe(self._on_yaxis_change, names=['min', 'max'])

        def initialize_toolbar(self):
            self.toolbar = Toolbar(self)

            for tool_id in viewer_tools:
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

        def _on_xaxis_change(self, change):
            self.update_xticks(**{ change["name"] : change["new"] })

        def _on_yaxis_change(self, change):
            self.update_yticks(**{ change["name"] : change["new"] })

        def update_nxticks(self, nticks):
            if nticks == self.nxticks:
                return
            self.nxticks = max(nticks, 1)
            self.update_xticks()

        def update_nyticks(self, nticks):
            if nticks == self.nyticks:
                return
            self.nyticks = max(nticks, 1)
            self.update_yticks()

        def update_xticks(self, min=None, max=None):
            min = min or self.state.x_min
            max = max or self.state.x_max
            if min is None or max is None:
                return
            x_range = max - min
            frac = int(x_range / self.nxticks)
            spacing = next((t for t in self.TICK_SPACINGS if frac > t), self.TICK_SPACINGS[-1])
            self.set_xtick_spacing(spacing)

        def update_yticks(self, min=None, max=None):
            min = min or self.state.y_min
            max = max or self.state.y_max
            if min is None or max is None:
                return
            y_range = max - min
            frac = int(y_range / self.nyticks)
            spacing = next((t for t in self.TICK_SPACINGS if frac > t), self.TICK_SPACINGS[-1])
            self.set_ytick_spacing(spacing)

        def set_xtick_spacing(self, spacing):
            xmin, xmax = self.state.x_min, self.state.x_max
            tmin = ceil(xmin / spacing) * spacing
            tmax = floor(xmax / spacing) * spacing
            n = int((tmax - tmin) / spacing) + 1
            self.axis_x.tick_values = list(linspace(tmin, tmax, n))

        def set_ytick_spacing(self, spacing):
            ymin, ymax = self.state.y_min, self.state.y_max
            tmin = ceil(ymin / spacing) * spacing
            tmax = floor(ymax / spacing) * spacing
            n = int((tmax - tmin) / spacing) + 1
            self.axis_y.tick_values = list(linspace(tmin, tmax, n))
        
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
