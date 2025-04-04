from uuid import uuid4

from numpy import isfinite
from plotly.graph_objs import Scatter

from glue.core import BaseData

from glue_plotly.common import color_info, dimensions, fixed_color

from glue_plotly.viewers.histogram.dotplot_layer_artist import PlotlyDotplotLayerArtist


from typing import Literal

__all__ = ["CDSPlotlyDotplotLayerArtist"]


# glue_plotly/common/dotplot.py
def dot_radius(viewer, layer_state):
    edges = layer_state.histogram[0]
    viewer_state = viewer.state
    diam_world = min([edges[i + 1] - edges[i] for i in range(len(edges) - 1)])
    width, height = dimensions(viewer)
    diam = diam_world * width / abs(viewer_state.x_max - viewer_state.x_min)
    if viewer_state.y_min is not None and viewer_state.y_max is not None and viewer_state.y_min != viewer_state.y_max:
        max_diam_world_v = 1
        diam_pixel_v = max_diam_world_v * height / abs(viewer_state.y_max - viewer_state.y_min)
        diam = min(diam_pixel_v, diam)
    if not isfinite(diam):
        diam = 1
    # return diam / 2 # default
    return diam * 3 # obviously using the new one

# glue_plotly/common/dotplot.py
def dot_positions(layer_state):
    x = []
    y = []
    edges, counts = layer_state.histogram
    counts = counts.astype(int)
    for i in range(len(edges) - 1):
        x_i = (edges[i] + edges[i + 1]) / 2
        y_i = range(1, counts[i] + 1)
        x.extend([x_i] * counts[i])
        y.extend(y_i)

    return x, y

# glue_plotly/common/dotplot.py
def dots_for_layer(viewer, layer_state, add_data_label=True):
    legend_group = uuid4().hex
    dots_id = uuid4().hex

    x, y = dot_positions(layer_state)

    radius = dot_radius(viewer, layer_state)
    marker = dict(color=color_info(layer_state, mask=None), size=radius)

    name = layer_state.layer.label
    if add_data_label and not isinstance(layer_state.layer, BaseData):
        name += " ({0})".format(layer_state.layer.data.label)

    return Scatter(
        x=x,
        y=y,
        mode="markers",
        marker=marker,
        name=name,
        legendgroup=legend_group,
        meta=dots_id,
    )


# Override the PlotlyDotplotLayerArtist
# Use CDSPlotlyDotplotLayerArtist in viewer.py for _data_artist_cls and _subset_artist_cls
class CDSPlotlyDotplotLayerArtist(PlotlyDotplotLayerArtist):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _update_visual_attrs_for_trace(self, trace):
        marker = trace.marker
        marker.update(opacity=self.state.alpha, color=fixed_color(self.state), size=dot_radius(self.view, self.state))
        trace.update(marker=marker,
                     visible=self.state.visible,
                     unselected=dict(marker=dict(opacity=self.state.alpha)))
        
    def _create_dots(self):
        dots = dots_for_layer(self.view, self.state, add_data_label=True)
        dots.update(hoverinfo='all', unselected=dict(marker=dict(opacity=self.state.alpha)))
        self._dots_id = dots.meta if dots else None
        return dots


