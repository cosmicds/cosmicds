import json
import os

import numpy as np
from traitlets import Unicode

__all__ = ['component_value_subsets', 'load_template', 'update_figure_css']

def component_value_subsets(data, component_name, labeler=None):
    """
    This function creates a subset for entries with each value
    of a given component, and returns a list of these subsets.
    
    Parameters
    ----------
    data : glue.core.data.Data
        The glue data object for which subsets will be created.
    component_name : str
        The name of the component along which we want to partition
        the data into subsets.
    labeler: (any) -> str:
        A function to create a label for each subset, based on the
        value used to create it.

    Returns
    -------
    List[glue.core.data.Data]
        A list of the created subsets.
    """
    return [data.new_subset(data.id[component_name] == x, label=labeler(x)) for x in np.unique(data[component_name])]


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
            viewer_prop = getattr(viewer.layers[0], prop)
            setattr(viewer_prop, k, v)
