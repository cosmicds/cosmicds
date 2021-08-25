import json
import os

from astropy import units as u
from bqplot.scales import LinearScale
from bqplot_image_gl import LinesGL
from glue_jupyter.bqplot.scatter.layer_artist import BqplotScatterLayerArtist
import numpy as np
from traitlets import Unicode

try:
    from astropy.cosmology import Planck18 as planck
except ImportError:
    from astropy.cosmology import Planck15 as planck

__all__ = ['age_in_gyr', 'load_template', 'update_figure_css', 'line_mark', 'vertical_line_mark']


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

def load_template(file_name, path=None, traitlet=True):
    """
    Load a vue template file and instantiate the appropriate traitlet object.

    Parameters
    ----------
    file_name : str
        The name of the template file.
    path : str
        The path to where the template file is stored. If none is given,
        assumes the directory where the python file calling this function
        resides.

    Returns
    -------
    `Unicode`
        The traitlet object used to hold the vue code.
    """
    path = os.path.dirname(path)

    with open(os.path.join(path, file_name)) as f:
        TEMPLATE = f.read()

    if traitlet:
        return Unicode(TEMPLATE)

    return TEMPLATE


def update_figure_css(viewer, style_dict=None, style_path=None):
    """
    Update the css of a BqPlot `~bqplot.figure.Figure` object.

    Parameters
    ----------
    viewer : `~glue_jupyter.bqplot.scatter.viewer.BqplotScatterView`
        The glue jupyter BqPlot viewer wrapper instance.
    style_dict : dict
        A dictionary containing the css attributes to be updated.
    style_path : string or `~pathlib.Path`
        A path to the ``.json`` file containing the css attributes to be
        parsed into a dictionary.
    """
    figure = viewer.figure_widget

    if style_path is not None:
        with open(style_path) as f:
            style_dict = json.load(f)

    fig_styles = style_dict.get('figure')
    viewer_styles = style_dict.get('viewer')

    # Update figure styles
    for k, v in fig_styles.items():
        # Update axes styles
        if k == 'axes':
            for ak, av in fig_styles.get('axes')[0].items():
                if ak == 'tick_values':
                    av = np.array(av)

                setattr(figure.axes[0], ak, av)

            for ak, av in fig_styles.get('axes')[1].items():
                if ak == 'tick_values':
                    av = np.array(av)

                setattr(figure.axes[1], ak, av)
        else:
            setattr(figure, k, v)

    # Update viewer styles
    for prop in viewer_styles:
        for k, v in viewer_styles.get(prop, {}).items():
            is_list = isinstance(v, list)
            for (index, layer) in enumerate(viewer.layers):
                viewer_prop = getattr(layer, prop)
                val = v[index % len(v)] if is_list else v
                setattr(viewer_prop, k, val)

def line_mark(layer, start_x, start_y, end_x, end_y, color):
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
        layer_scales = layer.image.scales
    else:
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
                   labels_visibility='label')

def vertical_line_mark(layer, x, color):
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
    return line_mark(layer, x, viewer_state.y_min, x, viewer_state.y_max, color)
