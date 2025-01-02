from glue.core import Data
from glue_plotly.viewers.histogram import PlotlyHistogramView
from glue_plotly.viewers.histogram.dotplot_layer_artist import PlotlyDotplotLayerArtist

from cosmicds.viewers.dotplot.state import DotPlotViewerState
from cosmicds.viewers.dotplot.scatter_layer_artist import DotplotScatterLayerArtist 

from typing import Literal

__all__ = ["PlotlyDotPlotView"]


class PlotlyDotPlotView(PlotlyHistogramView):

    LABEL = "Dot Plot Viewer"

    _state_cls = DotPlotViewerState
    _data_artist_cls = PlotlyDotplotLayerArtist
    _subset_artist_cls = PlotlyDotplotLayerArtist

    _scatter_layers = set()

    def add_data(self, data: Data, layer_type: Literal["dotplot"] | Literal["scatter"] = "dotplot"):
         
        if layer_type == "scatter":
            self._scatter_layers.add(data.uuid)

        return super().add_data(data)

    # def add_subset(self, data: Data, layer_type: Literal["dotplot"] | Literal["scatter"] = "dotplot"):
    #     if layer_type == "scatter":
    #         self._scatter_layers.add(data.uuid)
    #     super().add_subset(data)

    def get_data_layer_artist(self, layer=None, layer_state=None):
        if layer is not None and layer.uuid in self._scatter_layers:
            return DotplotScatterLayerArtist(self, self.state, layer_state=layer_state, layer=layer)
        return super().get_data_layer_artist(layer, layer_state)

    # For now, subsets have the same layer type as their parent
    def get_subset_layer_artist(self, layer=None, layer_state=None):
        if layer is not None and layer.data.uuid in self._scatter_layers:
            return DotplotScatterLayerArtist(self, self.state, layer_state=layer_state, layer=layer)
        return super().get_subset_layer_artist(layer, layer_state)
