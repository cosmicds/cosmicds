import numpy as np

from glue.core import BaseData, Subset

from glue.config import colormaps
from glue.viewers.matplotlib.state import (MatplotlibLayerState,
                                           DeferredDrawCallbackProperty as DDCProperty,
                                           DeferredDrawSelectionCallbackProperty as DDSCProperty)
from glue.core.state_objects import StateAttributeLimitsHelper
from echo import keep_in_sync, delay_callback
from glue.core.data_combo_helper import ComponentIDComboHelper, ComboHelper
from glue.core.exceptions import IncompatibleAttribute
from glue.viewers.common.stretch_state_mixin import StretchStateMixin


__all__ = ['ScatterLayerState']


class ScatterLayerState(MatplotlibLayerState, StretchStateMixin):
    """
    A state class that includes all the attributes for layers in a scatter plot.
    """

    # Color

    cmap_mode = DDSCProperty(docstring="Whether to use color to encode an attribute")
    cmap_att = DDSCProperty(docstring="The attribute to use for the color")
    cmap_vmin = DDCProperty(docstring="The lower level for the colormap")
    cmap_vmax = DDCProperty(docstring="The upper level for the colormap")
    cmap = DDCProperty(docstring="The colormap to use (when in colormap mode)")

    # Markers

    markers_visible = DDCProperty(True, docstring="Whether to show markers")
    size = DDCProperty(docstring="The size of the markers")
    size_mode = DDSCProperty(docstring="Whether to use size to encode an attribute")
    size_att = DDSCProperty(docstring="The attribute to use for the size")
    size_vmin = DDCProperty(docstring="The lower level for the size mapping")
    size_vmax = DDCProperty(docstring="The upper level for the size mapping")
    size_scaling = DDCProperty(1, docstring="Relative scaling of the size")
    fill = DDCProperty(True, docstring="Whether to fill the markers")

    # Density map

    density_map = DDCProperty(False, docstring="Whether to show the points as a density map")
    density_contrast = DDCProperty(1, docstring="The dynamic range of the density map")

    # Note that we keep the dpi in the viewer state since we want it to always
    # be in sync between layers.

    # Line

    line_visible = DDCProperty(False, docstring="Whether to show a line connecting all positions")
    linewidth = DDCProperty(1, docstring="The line width")
    linestyle = DDSCProperty(docstring="The line style")

    def __init__(self, viewer_state=None, layer=None, **kwargs):

        super(ScatterLayerState, self).__init__(viewer_state=viewer_state, layer=layer)

        self.limits_cache = {}

        self.cmap_lim_helper = StateAttributeLimitsHelper(self, attribute='cmap_att',
                                                          lower='cmap_vmin', upper='cmap_vmax',
                                                          limits_cache=self.limits_cache)

        self.size_lim_helper = StateAttributeLimitsHelper(self, attribute='size_att',
                                                          lower='size_vmin', upper='size_vmax',
                                                          limits_cache=self.limits_cache)

        self.cmap_att_helper = ComponentIDComboHelper(self, 'cmap_att',
                                                      numeric=True, datetime=False, categorical=False)

        self.size_att_helper = ComponentIDComboHelper(self, 'size_att',
                                                      numeric=True, datetime=False, categorical=False)

        ScatterLayerState.cmap_mode.set_choices(self, ['Fixed', 'Linear'])
        ScatterLayerState.size_mode.set_choices(self, ['Fixed', 'Linear'])

        linestyle_display = {'solid': '–––––––',
                             'dashed': '– – – – –',
                             'dotted': '· · · · · · · ·',
                             'dashdot': '– · – · – ·'}

        ScatterLayerState.linestyle.set_choices(self, ['solid', 'dashed', 'dotted', 'dashdot'])
        ScatterLayerState.linestyle.set_display_func(self, linestyle_display.get)

        self.setup_stretch_callback()
        self.stretch = 'log'


        self.add_callback('layer', self._on_layer_change)
        if layer is not None:
            self._on_layer_change()

        self.cmap = colormaps.members[0][1]
        self.add_callback('cmap_att', self._check_for_preferred_cmap)

        self.size = self.layer.style.markersize

        self._sync_size = keep_in_sync(self, 'size', self.layer.style, 'markersize')

        self.update_from_dict(kwargs)

    def _check_for_preferred_cmap(self, *args):
        if isinstance(self.layer, BaseData):
            layer = self.layer
        else:
            layer = self.layer.data
        actual_component = layer.get_component(self.cmap_att)
        if getattr(actual_component, 'preferred_cmap', False):
            self.cmap = actual_component.preferred_cmap

    def _on_layer_change(self, layer=None):

        with delay_callback(self, 'cmap_vmin', 'cmap_vmax', 'size_vmin', 'size_vmax'):

            if self.layer is None:
                self.cmap_att_helper.set_multiple_data([])
                self.size_att_helper.set_multiple_data([])
            else:
                self.cmap_att_helper.set_multiple_data([self.layer])
                self.size_att_helper.set_multiple_data([self.layer])

    def flip_cmap(self):
        """
        Flip the cmap_vmin/cmap_vmax limits.
        """
        self.cmap_lim_helper.flip_limits()

    def flip_size(self):
        """
        Flip the size_vmin/size_vmax limits.
        """
        self.size_lim_helper.flip_limits()

    @property
    def cmap_name(self):
        return colormaps.name_from_cmap(self.cmap)

    @classmethod
    def __setgluestate__(cls, rec, context):
        # Patch for glue files produced with glue v0.11
        if 'style' in rec['values']:
            style = context.object(rec['values'].pop('style'))
            if style == 'Scatter':
                rec['values']['markers_visible'] = True
                rec['values']['line_visible'] = False
            elif style == 'Line':
                rec['values']['markers_visible'] = False
                rec['values']['line_visible'] = True
        return super(ScatterLayerState, cls).__setgluestate__(rec, context)
