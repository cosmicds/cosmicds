from cosmicds.utils import vertical_line_mark

from itertools import chain
import solara
from solara import Reactive
from solara import component_vue
import reacton.ipyvuetify as rv
from uuid import uuid4

from glue.core import Data
from glue.viewers.common.viewer import Viewer
from glue_plotly.viewers.common import PlotlyBaseView
from plotly.graph_objects import Scatter
from numbers import Number
from typing import Callable, Iterable, List, Optional

from ..utils import line_mark, mode, CDS_IMAGE_BASE_URL

image_location=f"{CDS_IMAGE_BASE_URL}"

# glue doesn't implement a mode statistic, so we roll our own
# Since there can be multiple modes, mode can be a list
# and so we return a list for every statistic to make things simpler
def find_statistic(stat: str, viewer: Viewer, data: Data, bins: Iterable[int | float] | None):
    if stat == "mode":
        return mode(data, viewer.state.x_att, bins=bins, range=[viewer.state.hist_x_min, viewer.state.hist_x_max])
    else:
        return [data.compute_statistic(stat, viewer.state.x_att)]


# TODO: How can we make this more general to put into the utilities?
def labeled_vertical_line(x: float, y_min: float, y_max: float, color: str, label: str | None, unit: Optional[str] = None, label_position: Optional[float] = None):
    label_position = label_position or 0.85
    text = f"{label} {unit}" if unit else label
    return Scatter(
        x=[x, x, x],
        y=[y_min, label_position * (y_max - y_min), y_max],
        mode="text+lines",
        line=dict(color=color),
        name=label,
        text=['', f'  {text}', ''],
        textposition="top right",
    )


@solara.component
def StatisticsSelector(viewers: List[PlotlyBaseView],
                       glue_data: List[Data],
                       units: List[str],
                       bins: None | List[None | Iterable[Number]]=None,
                       statistics: List[str]=["mean", "median", "mode"],
                       transform: Callable[[Number], Number] | None=None,
                       **kwargs):

    selected = solara.use_reactive(None)
    viewer_labels, set_viewer_labels = solara.use_state([])
    color = kwargs.get("color", "#f00")
    bins = bins or [getattr(viewer.state, "bins", None) for viewer in viewers]

    help_text = {
        "mean": "The mean is the average of all values in the dataset. The average is calculated by adding all the values together and dividing by the number of values. In this example, the mean of the distribution is 14.",
        "median": "The median is the middle of the dataset. Fifty percent of the data has values greater than the median and fifty percent has values less than or equal to the median. In this example, the median of the distribution is 15.",
        "mode": "The mode is the most commonly measured value or range of values in a set of data and appears as the tallest bar in a histogram. In this example, the mode of the distribution is 16.",
    }
    help_images = {
        "mean": f"{image_location}/mean.png",
        "median": f"{image_location}/median.png",
        "mode": f"{image_location}/mode.png",
    }

    alt_text = {
        "mean": "A histogram with a range of 9 through 18, with counts from 0 through 8. The mean is highlighted in red.",
        "median": "A histogram with a range of 9 through 18, with counts from 0 through 8. The median is highlighted in red. Because the distribution is skewed to the right, the median is slightly to the right of center.",
        "mode": "A histogram with a range of 9 through 18, with counts from 0 through 8. The mode has the highest count and is highlighted in red.",
    }

    last_updated = selected.value 

    def _line_ids_for_viewer(viewer: PlotlyBaseView):
        line_ids = []
        traces = list(chain(l.traces() for l in viewer.layers))
        for trace in viewer.figure.data:
            if trace not in traces and isinstance(trace, Scatter) and getattr(trace, "meta", None):
                line_ids.append(trace.meta)

        return line_ids

    line_ids = [_line_ids_for_viewer(viewer) for viewer in viewers]

    def _remove_lines():
        for (viewer, viewer_line_ids) in zip(viewers, line_ids):
            lines = list(viewer.figure.select_traces(lambda t: t.meta in viewer_line_ids))
            viewer.figure.data = [t for t in viewer.figure.data if t not in lines]

    def _clear_viewer_label(index):
        viewer = viewers[index]
        try:
            viewer.state.subtitle = viewer.state.subtitle.replace(viewer_labels[index], "")
        except IndexError:
            pass

    def _update_lines():
        stat = selected.value
        if last_updated == stat:
            return stat

        if last_updated is not None:
            _remove_lines()

        if stat is None:
            for index, viewer in enumerate(viewers):
                _clear_viewer_label(index)
            set_viewer_labels([])
            return None

        line_ids.clear()
        labels = []
        for index, (viewer, d, bin, unit) in enumerate(zip(viewers, glue_data, bins, units)):
            _clear_viewer_label(index)
            viewer_lines = []
            viewer_line_ids = []
            try:
                capitalized = stat.capitalize()
                values = find_statistic(stat, viewer, d, bin)
                if transform is not None:
                    values = [transform(v) for v in values]
                multiple_values = len(values) > 1
                if multiple_values:
                    # NB: If we at some point have a non-trivial (i.e. not just "add an s")
                    # plural, we will need to update this - maybe using e.g. the inflect package
                    viewer_label = f"{capitalized}s: {', '.join(str(v) for v in values)}"
                    if unit:
                        viewer_label += f" {unit}"
                    if viewer.state.subtitle:
                        viewer_label = viewer_label + (" " * 10)
                    viewer.state.subtitle = viewer_label + viewer.state.subtitle
                    labels.append(viewer_label)

                for value in values:
                    if not multiple_values:
                        label = f"{capitalized}: {value}"
                        if unit:
                            label += f" {unit}"
                    else:
                        label = ""
                    line = labeled_vertical_line(value, viewer.state.y_min, viewer.state.y_max,
                                                 color, label=label, unit=None)
                    line_id = str(uuid4())
                    line["meta"] = line_id
                    viewer_lines.append(line)
                    viewer_line_ids.append(line_id)
            except ValueError as e:
                print(e)

            # The Scatter traces that get added aren't the same instances
            # as those we pass in. So we need to grab references to them
            # AFTER they've been added
            viewer.figure.add_traces(viewer_lines)
            line_ids.append(viewer_line_ids)

        set_viewer_labels(labels)

        return stat

    def _update_selected(stat: str | None, value: bool):
        nonlocal last_updated
        if value:
            selected.set(stat)
        elif selected.value == stat:
            selected.set(None)
        last_updated = _update_lines()

    def _model_factory(stat: str):
        return solara.lab.computed(lambda stat=stat: selected.value == stat)

    from cosmicds.components import InfoDialog

    with rv.Card(class_="switch-panel", outlined=True):
        with rv.Container():
            for stat in statistics:
                model = _model_factory(stat)
                with solara.Row(style={"align-items": "center"}, classes=["switch-panel"]):
                    solara.Switch(value=model,
                                  label=stat.capitalize(),
                                  on_value=lambda value, stat=stat: _update_selected(stat, value))
                    InfoDialog(
                        dialog=False,
                        title=stat,
                        content=help_text[stat],
                        hasImage=True,
                        image=help_images[stat],
                        altText=alt_text[stat],
                    )
