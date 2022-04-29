# This file is for viewers that don't need anything beyond
# the standard CDS updating (the new toolbar, etc.)

from glue.config import viewer_tool
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.bqplot.histogram import BqplotHistogramView

from cosmicds.components.toolbar import Toolbar

def cds_viewer(viewer_class, name=None, viewer_tools=None, label=None, state_cls=None):
    class CDSViewer(viewer_class):

        __name__ = name
        __qualname__ = name
        _state_cls = state_cls or viewer_class._state_cls
        inherit_tools = viewer_tools is None
        tools = viewer_tools or viewer_class.tools
        LABEL = label or viewer_class.LABEL

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ignore_conditions = []

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
                return
            super().add_data(data)

        def add_subset(self, subset):
            if any(condition(subset) for condition in self.ignore_conditions):
                return
            super().add_subset(subset)
        
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
