from collections import Counter
from ipyvuetify import VuetifyTemplate
from numpy import amax, flatnonzero, histogram
from traitlets import Dict, List, Unicode, observe

from ...utils import load_template, vertical_line_mark

class StatisticsSelector(VuetifyTemplate):

    template = load_template("statistics_selector.vue", __file__, traitlet=True).tag(sync=True)
    color = Unicode("#1e90ff").tag(sync=True)
    selected = Unicode(None, allow_none=True).tag(sync=True)
    statistics = List().tag(sync=True)
    was_selected = Unicode(allow_none=True).tag(sync=True)

    help_text = Dict({
        "mode": "Description of the mode",
        "mean": "Description of the mean",
        "median": "Description of the median"
    }).tag(sync=True)

    help_images = Dict({
        "mode": "path to mode image",
        "mean": "path to mean image",
        "median": "path to median image"
    }).tag(sync=True)

    def __init__(self, viewers, data, statistics=['mean', 'median', 'mode'], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewers = viewers
        self.glue_data = data
        self.statistics = statistics
        self.transform = kwargs.get("transform", None)
        self._bins = kwargs.get("bins", None)
        self.lines = []
        if "color" in kwargs:
            self.color = kwargs["color"]
        if "units" in kwargs:
            self.units = kwargs["units"]
        for (index, viewer) in enumerate(self.viewers):
            viewer.figure.observe(lambda _change: self._on_marks_updated(index), names=["marks"])

    def _mode(self, viewer, data, bins):
        component_id = viewer.state.x_att
        values = data[component_id]
        if bins is not None:
            hist, hbins = histogram(values, bins=bins)
            indices = flatnonzero(hist == amax(hist)) 
            return [0.5 * (hbins[idx] + hbins[idx + 1]) for idx in indices]
        else:
            counter = Counter(data)
            max_count = counter.most_common(1)[0][1]
            return [k for k, v in counter.items() if v == max_count]

    # glue doesn't implement a mode statistic, so we roll our own
    # Since there can be multiple modes, mode can be a list
    # and so we return a list for every statistic to make things simpler
    def _find_statistic(self, stat, viewer, data, bins):
        if stat == 'mode':
            return self._mode(viewer, data, bins)
        else:
            return [data.compute_statistic(stat, viewer.state.x_att)]

    @property
    def bins(self):
        if self._bins is not None:
            return self._bins
        return [getattr(viewer.state, "bins", None) for viewer in self.viewers] 

    # This is a bit of a hack to prevent layer artists from
    # redrawing their marks without ours included
    def _on_marks_updated(self, index):
        if not self.lines:
            return
        line = self.lines[index]
        viewer = self.viewers[index]
        if line is not None and line not in viewer.figure.marks:
            viewer.figure.marks = viewer.figure.marks + [line]

    def _remove_lines(self):
        if self.lines:
            # Do this first so that _on_marks_updated doesn't redraw the lines
            lines = self.lines
            self.lines = []
            
            for (viewer, line) in zip(self.viewers, lines):
                viewer.figure.marks = [m for m in viewer.figure.marks if m is not line]

    @observe('selected')
    def _update_marks(self, change):
        selected = change["new"]
        self._remove_lines()

        if selected is None:
            return

        lines = []
        for viewer, data, bins, unit in zip(self.viewers, self.glue_data, self.bins, self.units):
            try:
                values = self._find_statistic(selected, viewer, data, bins)
                if self.transform is not None:
                    values = [self.transform(v) for v in values]
                for value in values:
                    label = f"{selected.capitalize()}: {value}"
                    if unit:
                        label += f" {unit}"
                    line = vertical_line_mark(viewer.layers[0], value, self.color,
                                          label=label, label_visibility="none")
            except ValueError:
                line = None 

            lines.append(line)
            line_mark_list = [line] if line is not None else []
            viewer.figure.marks = viewer.figure.marks + line_mark_list

        self.lines = lines

