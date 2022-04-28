# This file is for viewers that don't need anything beyond
# the standard CDS updating (the new toolbar, etc.)

from glue.config import viewer_tool
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.bqplot.histogram import BqplotHistogramView

from cosmicds.components.toolbar import Toolbar

def cds_viewer(viewer_class, viewer_tools, label=None):
    class CDSViewer(viewer_class):

        inherit_tools = False
        tools = viewer_tools
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


CDSScatterView = cds_viewer(BqplotScatterView, ['bqplot:home', 'bqplot:rectzoom', 'bqplot:rectangle'], '2D scatter')
CDSHistogramView = cds_viewer(BqplotHistogramView, ['bqplot:home', 'bqplot:xzoom', 'bqplot:xrange'], 'Histogram')
