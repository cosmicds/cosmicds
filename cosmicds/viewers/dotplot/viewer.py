from glue_jupyter.bqplot.histogram import BqplotHistogramView
from .layer_artist import BqplotDotPlotLayerArtist
from .state import DotPlotViewerState

class BqplotDotPlotView(BqplotHistogramView):

    LABEL = "Dot Plot Viewer"

    _state_cls = DotPlotViewerState
    _data_artist_cls = BqplotDotPlotLayerArtist
    _subset_artist_cls = BqplotDotPlotLayerArtist

    tools = ["bqplot:home", "bqplot:xzoom"]

    def __init__(self, session, state=None):
        super(BqplotDotPlotView, self).__init__(session, state=state)
        self.figure.layout.observe(self._update_height, names='height')

    def _update_height(self, change):
        # For now, we just assume that the height is entered in pixels
        # e.g. "300px"
        # TODO: Handle other height specifications
        height = change["new"]
        if height.endswith("px"):
            height = int(height[:-2])
            height -= self.figure.fig_margin["bottom"]
            self.state.viewer_height = height
