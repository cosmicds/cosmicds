import json
import os

import numpy as np
from threading import Timer
from traitlets import Unicode

__all__ = [
    'load_template', 'update_figure_css', 'extend_tool',
    'RepeatedTimer'
]

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
