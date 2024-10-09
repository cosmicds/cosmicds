from itertools import chain
from uuid import uuid4

from glue_plotly.common import color_info
from glue_plotly.common.scatter2d import scatter_mode, size_info
from glue.core import BaseData
from glue.core.exceptions import IncompatibleAttribute
from glue.utils import ensure_numerical
from glue.viewers.common.layer_artist import LayerArtist

from plotly.graph_objs import Scatter

from cosmicds.viewers.dotplot.scatter_layer_state import ScatterLayerState


__all__ = ["DotplotScatterLayerArtist"]


CMAP_PROPERTIES = {"cmap_mode", "cmap_att", "cmap_vmin", "cmap_vmax", "cmap"}
MARKER_PROPERTIES = {
    "size_mode",
    "size_att",
    "size_vmin",
    "size_vmax",
    "size_scaling",
    "size",
    "fill",
}
DENSITY_PROPERTIES = {"dpi", "stretch", "density_contrast"}
VISUAL_PROPERTIES = (
    CMAP_PROPERTIES
    | MARKER_PROPERTIES
    | DENSITY_PROPERTIES
    | {"color", "alpha", "zorder", "visible"}
)

LIMIT_PROPERTIES = {"x_min", "x_max"}
DATA_PROPERTIES = {
    "layer",
    "x_att",
    "cmap_mode",
    "size_mode",
    "density_map",
    "vector_visible",
    "vector_arrowhead",
    "vector_mode",
    "vector_origin",
    "line_visible",
    "markers_visible",
    "vector_scaling",
}


class DotplotScatterLayerArtist(LayerArtist):

    _layer_state_cls = ScatterLayerState

    def __init__(self, view, viewer_state, layer_state=None, layer=None):

        super().__init__(
            viewer_state,
            layer_state=layer_state,
            layer=layer,
        )

        self.view = view

        # Somewhat annoyingly, the trace that we pass in to be added
        # is NOT the same instance that ends up living in the figure.
        # (see basedatatypes.py line 2251 in the Plotly package)
        # So we abuse the metadata entry of the trace to tag it with
        # a UUID so that we can extract it when needed.
        # Note that setting the UID directly (either in the Scatter
        # constructor or after) doesn't seem to work - it gets
        # overridden by Plotly
        self._scatter_id = uuid4().hex
        scatter = self._create_scatter()
        self.view.figure.add_trace(scatter)

        # We want to initialize these to some dummy UUIDs so that
        # _get_lines, _get_error_bars, _get_vectors, etc. don't pick up
        # any other traces that tools have added to the viewer, which
        # will happen if these IDs are None
        self._lines_id = uuid4().hex
        self._error_id = uuid4().hex
        self._vector_id = uuid4().hex

        self._viewer_state.add_global_callback(self._update_display)
        self.state.add_global_callback(self._update_display)
        self.state.add_callback("zorder", self._update_zorder)

    def remove(self):
        self.view._remove_traces([self._get_scatter()])
        self.view._remove_traces(self._get_lines())
        self.view._remove_traces(self._get_error_bars())
        self.view._remove_traces(self._get_vectors())
        return super().remove()

    def _get_traces_with_id(self, id):
        return self.view.figure.select_traces(dict(meta=id))

    def _get_scatter(self):
        # The scatter trace should always exist
        # so if somehow it doesn't, then create it
        try:
            return next(self._get_traces_with_id(self._scatter_id))
        except StopIteration:
            scatter = self._create_scatter()
            self.view.figure.add_trace(scatter)
            return scatter

    def _get_lines(self):
        return self._get_traces_with_id(self._lines_id)

    def _get_error_bars(self):
        return self._get_traces_with_id(self._error_id)

    def _get_vectors(self):
        return self._get_traces_with_id(self._vector_id)

    def traces(self):
        return chain([self._get_scatter()], self._get_lines(), self._get_error_bars(), self._get_vectors())

    def _update_data(self):

        try:
            x = ensure_numerical(self.layer[self._viewer_state.x_att].ravel())
        except (IncompatibleAttribute, IndexError):
            if self._viewer_state.x_att is not None:
                self.disable_invalid_attributes(self._viewer_state.x_att)
            return
        else:
            self.enable()

        scatter = self._get_scatter()
        scatter.update(x=x, y=[self.state.height for _ in x])

    def _create_scatter(self):
        if isinstance(self.layer, BaseData):
            name = self.layer.label
        else:
            name = f"{self.layer.label} ({self.layer.data.label})"

        scatter_info = dict(mode=scatter_mode(self.state),
                            name=name,
                            hoverinfo='all',
                            unselected=dict(marker=dict(opacity=self.state.alpha)),
                            meta=self._scatter_id)
        scatter = Scatter(**scatter_info)
        return scatter

    def _update_display(self, force=False, **kwargs):
        changed = self.pop_changed_properties()

        if 'layout_update' in kwargs:
            self.view._clear_traces()
            scatter = self._create_scatter()
            self.view.figure.add_trace(scatter)
            force = True

        if force or len(changed & DATA_PROPERTIES) > 0:
            self._update_data()
            force = True

        if force or len(changed & VISUAL_PROPERTIES) > 0:
            self._update_visual_attributes(changed, force=force)

    def _update_zorder(self, *args):
        current_traces = self.view.figure.data
        traces = [self.view.selection_layer]
        for layer in self.view.layers:
            traces += list(layer.traces())
        self.view.figure.data = traces + [t for t in current_traces if t not in traces]

    def _update_visual_attributes(self, changed, force=False):

        if not self.enabled:
            return

        # Only run select_traces once
        scatter = self._get_scatter()

        if self.state.markers_visible:
            if force or \
                    any(prop in changed for prop in CMAP_PROPERTIES) or \
                    any(prop in changed for prop in ["color", "fill"]):

                color = color_info(self.state)
                if self.state.fill:
                    scatter.marker.update(color=color,
                                          line=dict(width=0),
                                          opacity=self.state.alpha)
                else:
                    scatter.marker.update(color='rgba(0, 0, 0, 0)',
                                          opacity=self.state.alpha,
                                          line=dict(width=1,
                                                    color=color)
                                          )

            if force or any(prop in changed for prop in MARKER_PROPERTIES):
                scatter.marker['size'] = size_info(self.state)

        if force or "alpha" in changed:
            marker = scatter.marker
            opacity_dict = dict(opacity=self.state.alpha)
            marker.update(**opacity_dict)
            scatter.update(marker=marker,
                           unselected=dict(marker=opacity_dict))

        if force or "visible" in changed:
            scatter.visible = self.state.visible

    def update(self, **kwargs):
        self._update_display(force=True, **kwargs)
