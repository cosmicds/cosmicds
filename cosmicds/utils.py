import json
import os

import ipyvuetify as v
from astropy import units as u
from bqplot.scales import LinearScale
from bqplot_image_gl import LinesGL
from glue_jupyter.bqplot.histogram.layer_artist import BqplotHistogramLayerArtist
from glue_jupyter.bqplot.scatter.layer_artist import BqplotScatterLayerArtist
import numpy as np
from traitlets import Unicode
from threading import Timer

try:
    from astropy.cosmology import Planck18 as planck
except ImportError:
    from astropy.cosmology import Planck15 as planck

__all__ = [
    'MILKY_WAY_SIZE_MPC', 'RepeatedTimer',
    'age_in_gyr', 'load_template', 'update_figure_css',
     'extend_tool', 'format_fov', 'format_measured_angle',
    'line_mark', 'vertical_line_mark',
]

MILKY_WAY_SIZE_MPC = 0.03

# Both in angstroms
H_ALPHA_REST_LAMBDA = 6563
MG_REST_LAMBDA = 5177

GALAXY_FOV = 1.5 * u.arcmin
FULL_FOV = 60 * u.deg

def theme_colors():
    v.theme.dark = True
    v.theme.themes.dark.primary = 'colors.lightBlue.darken3'
    v.theme.themes.light.primary = 'colors.lightBlue.darken3'
    v.theme.themes.dark.secondary = 'colors.lightBlue.darken4'
    v.theme.themes.light.secondary = 'colors.lightBlue.darken4'
    v.theme.themes.dark.accent = 'colors.amber.accent2'
    v.theme.themes.light.accent = 'colors.amber.accent3'
    v.theme.themes.dark.info = 'colors.deepOrange.darken3'
    v.theme.themes.light.info = 'colors.deepOrange.lighten2'
    v.theme.themes.dark.success = 'colors.green.accent2'
    v.theme.themes.light.success = 'colors.green.accent2'
    v.theme.themes.dark.warning = 'colors.lightBlue.darken4'
    v.theme.themes.light.warning = 'colors.lightBlue.lighten4'
    v.theme.themes.dark.anchor = ''
    v.theme.themes.light.anchor = ''

# JC: I got this from https://stackoverflow.com/a/13151299
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

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
    
    # Not every tool has both activate and deactivate functions
    # e.g. the home tool doesn't have deactivate
    activate = getattr(tool, 'activate', None)
    deactivate = getattr(tool, 'deactivate', None)

    def extended_activate():
        if activate_cb:
            activate_cb()
        if activate:
            activate()

    def extended_deactivate():
        if deactivate:
            deactivate()
        if deactivate_cb:
            deactivate_cb()
    
    if activate or extended_activate:
        tool.activate = extended_activate
    if deactivate or extended_activate:
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
