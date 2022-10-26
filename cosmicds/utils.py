import json
import os
from math import log10

from astropy.modeling import models, fitting
from bqplot.marks import Lines
from bqplot.scales import LinearScale
from glue_jupyter.bqplot.histogram.layer_artist import BqplotHistogramLayerArtist
from glue_jupyter.bqplot.scatter.layer_artist import BqplotScatterLayerArtist
from glue.core.state_objects import State
import numpy as np
from threading import Timer
from traitlets import Unicode

__all__ = [
    'load_template', 'update_figure_css', 'extend_tool',
    'convert_material_color', 'fit_line', 
    'line_mark', 'vertical_line_mark',
    'API_URL', 'CDSJSONEncoder', 'RepeatedTimer',
    'debounce'
]

# The URL for the CosmicDS API
API_URL = "https://api.cosmicds.cfa.harvard.edu"


# JC: I got parts of this from https://stackoverflow.com/a/57915246
class CDSJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, State):
            return obj.as_dict()
        return super(CDSJSONEncoder, self).default(obj)


# JC: I got this from https://stackoverflow.com/a/13151299
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
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


def load_template(file_name, path=None, traitlet=False):
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


def convert_material_color(color_string):
    """
    This function converts the name of a material color, like those used in 
    ipyvuetify (e.g. colors.<base>.<lighten/darken#>) into a hex code.
    """
    from cosmicds.material_colors import MATERIAL_COLORS
    parts = color_string.split(".")[1:]
    result = MATERIAL_COLORS
    for part in parts:
        result = result[part]
    return result

def fit_line(x, y):
    fit = fitting.LinearLSQFitter()
    line_init = models.Linear1D(intercept=0, fixed={'intercept':True})
    fitted_line = fit(line_init, x, y)
    return fitted_line

def line_mark(layer, start_x, start_y, end_x, end_y, color, label=None):
    """
    Creates a Lines mark between the given start and end points
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
    return Lines(x=[start_x, end_x],
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

# Taken from https://jonlabelle.com/snippets/view/python/python-debounce-decorator-function
def debounce(wait):
    """Postpone a functions execution until after some time has elapsed
 
    :type wait: int
    :param wait: The amount of Seconds to wait before the next call can execute.
    """

    def decorator(fun):
        def debounced(*args, **kwargs):
            def call_it():
                fun(*args, **kwargs)

            try:
                debounced.t.cancel()
            except AttributeError:
                pass

            debounced.t = Timer(wait, call_it)
            debounced.t.start()

        return debounced

    return decorator

def frexp10(x, normed=False):
    """
    Find the mantissa and exponent of a value in base 10.

    If normed is True, the mantissa is fractional, while it is between 0 and 10 if normed is False.
    Example:
        normed: 0.5 * 10^5
        non-normed: 5 * 10^4

    TODO: JC added this quickly mid-Hubble beta. Are there possible improvements?
    """
    exp = int(log10(x)) + int(normed)
    mantissa = x / (10 ** exp)
    return mantissa, exp
