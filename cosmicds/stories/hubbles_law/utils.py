import json
import os

from astropy import units as u
from bqplot.scales import LinearScale
from bqplot_image_gl import LinesGL
from glue_jupyter.bqplot.histogram.layer_artist import BqplotHistogramLayerArtist
from glue_jupyter.bqplot.scatter.layer_artist import BqplotScatterLayerArtist
import numpy as np
from traitlets import Unicode

try:
    from astropy.cosmology import Planck18 as planck
except ImportError:
    from astropy.cosmology import Planck15 as planck

__all__ = [
    'age_in_gyr', 'extend_tool', 'line_mark', 'vertical_line_mark'
]


def age_in_gyr(H0):
    """
    Given a value for the Hubble constant, computes the age of the universe
    in Gyr, based on the Planck cosmology.

    Parameters
    ----------
    H0: float
        The value of the Hubble constant

    Returns
    ----------
    age: numpy.float64
        The age of the universe, in Gyr
    """
    age = planck.clone(H0=H0).age(0)
    unit = age.unit
    return age.value * unit.to(u.Gyr)


def extend_tool(viewer, tool_id, activate_cb=None, deactivate_cb=None):
    """
    This function extends the functionality of a tool on a viewer toolbar
    by adding callbacks that are activate upon tool item activation
    and deactivation.

    Parameters
    ----------
    viewer: `~glue.viewers.common.viewer.Viewer`
        The glue viewer whose tool we want to modify.
    tool_id: str
        The id of the tool that we want to modify - e.g. 'bqplot:xrange'
    activate_cb:
        The callback to be executed before the tool's `activate` method. Takes no arguments.
    deactivate_cb:
        The callback to be executed after the tool's `deactivate` method. Takes no arguments.

    """

    tool = viewer.toolbar.tools.get(tool_id, None)
    if not tool:
        return None

    activate = tool.activate
    deactivate = tool.deactivate

    def extended_activate():
        if activate_cb:
            activate_cb()
        activate()

    def extended_deactivate():
        deactivate()
        if deactivate_cb:
            deactivate_cb()

    tool.activate = extended_activate
    tool.deactivate = extended_deactivate


def format_fov(fov):
    return fov.to_string(unit=u.degree, sep=":", precision=0, pad=True) + " (dd:mm:ss)"


def format_measured_angle(angle):
    return angle.to_string(unit=u.arcsec, precision=0)[:-6] + " arcseconds"


def line_mark(layer, start_x, start_y, end_x, end_y, color, label=None):
    """
    Creates a LinesGL mark between the given start and end points
    using the scales of the given layer.

    Parameters
    ----------
    layer : `glue.viewers.common.layer_artist.LayerArtist`
        The layer used to determine the line's scales.
    start_x : int or float
        The x-coordinate of the line's starting point.
    start_y : int or float
        The y-coordinate of the line's starting point.
    end_x : int or float
        The x-coordinate of the line's endpoint.
    end_y : int or float
        The y-coordinate of the line's endpoint.
    color : str
        The desired color of the line, represented as a hex string.
    """
    if isinstance(layer, BqplotScatterLayerArtist):
        scales = layer.image.scales
    elif isinstance(layer, BqplotHistogramLayerArtist):
        layer_scales = layer.view.scales
        layer_x = layer_scales['x']
        layer_y = layer_scales['y']
        scales = {
            'x': LinearScale(min=layer_x.min, max=layer_x.max, allow_padding=layer_x.allow_padding),
            'y': LinearScale(min=layer_y.min, max=layer_y.max, allow_padding=layer_y.allow_padding),
        }
    return LinesGL(x=[start_x, end_x],
                   y=[start_y, end_y],
                   scales=scales,
                   colors=[color],
                   labels=[label] if label is not None else [],
                   display_legend=label is not None,
                   labels_visibility='label')


def vertical_line_mark(layer, x, color, label=None):
    """
    A specialization of `line_mark` specifically for vertical lines.

    Parameters
    ----------
    layer : `glue.viewers.common.layer_artist.LayerArtist`
        The layer used to determine the line's scales.
    x : int or float
        The x-coordinate of the vertical line
    color : str
        The desired color of the line, represented as a hex string.
    """
    viewer_state = layer.state.viewer_state
    return line_mark(layer, x, viewer_state.y_min, x, viewer_state.y_max, color, label)
