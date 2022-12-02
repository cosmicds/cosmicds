from glue_jupyter.bqplot.histogram import BqplotHistogramView
from .layer_artist import BqplotDotPlotLayerArtist
from .state import DotPlotViewerState

class BqplotDotPlotView(BqplotHistogramView):

    LABEL = "Dot Plot Viewer"

    _state_cls = DotPlotViewerState
    _data_artist_cls = BqplotDotPlotLayerArtist
    _subset_artist_cls = BqplotDotPlotLayerArtist

    tools = BqplotHistogramView.tools + ["bqplot:xzoom"]
