from glue_plotly.viewers.histogram import PlotlyHistogramView
from glue_plotly.viewers.histogram.dotplot_layer_artist import PlotlyDotplotLayerArtist

from cosmicds.viewers.dotplot.state import DotPlotViewerState

__all__ = ["PlotlyDotPlotView"]


class PlotlyDotPlotView(PlotlyHistogramView):

    LABEL = "Dot Plot Viewer"

    _state_cls = DotPlotViewerState
    _data_artist_cls = PlotlyDotplotLayerArtist
    _subset_artist_cls = PlotlyDotplotLayerArtist
