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

        def initialize_toolbar(self):
            self.toolbar = Toolbar(self)

            for tool_id in viewer_tools:
                mode_cls = viewer_tool.members[tool_id]
                mode = mode_cls(self)
                self.toolbar.add_tool(mode)
        
    return CDSViewer


CDSScatterView = cds_viewer(BqplotScatterView, ['bqplot:home', 'bqplot:rectzoom', 'bqplot:rectangle'], '2D scatter')
CDSHistogramView = cds_viewer(BqplotHistogramView, ['bqplot:home', 'bqplot:xzoom', 'bqplot:xrange'], 'Histogram')
