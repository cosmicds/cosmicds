# This file is for viewers that don't need anything beyond
# the standard CDS updating (the new toolbar, etc.)

from glue.config import viewer_tool
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.bqplot.histogram import BqplotHistogramView

from cosmicds.components.toolbar import Toolbar

def cds_viewer(ViewerClass, viewer_tools):
    class CDSViewer(ViewerClass):

        inherit_tools = False
        tools = viewer_tools

        def initialize_toolbar(self):
            self.toolbar = Toolbar(self)

            for tool_id in viewer_tools:
                mode_cls = viewer_tool.members[tool_id]
                mode = mode_cls(self)
                self.toolbar.add_tool(mode)
        
    return CDSViewer


CDSScatterView = cds_viewer(BqplotScatterView, ['bqplot:home', 'bqplot:rectzoom', 'bqplot:rectangle'])
CDSHistogramView = cds_viewer(BqplotHistogramView, ['bqplot:home', 'bqplot:xzoom', 'bqplot:xrange'])