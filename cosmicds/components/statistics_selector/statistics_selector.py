from collections import Counter
from ipyvuetify import VuetifyTemplate
from numpy import amax, flatnonzero, histogram
from traitlets import List, Unicode, observe

from ...utils import load_template, vertical_line_mark

class StatisticsSelector(VuetifyTemplate):

    template = load_template("statistics_selector.vue", __file__, traitlet=True).tag(sync=True)
    color = Unicode("#1e90ff").tag(sync=True)
    selected = Unicode(allow_none=True).tag(sync=True)
    statistics = List().tag(sync=True)
    unit = Unicode().tag(sync=True)
    was_selected = Unicode(allow_none=True).tag(sync=True)

    def __init__(self, viewer, data, component_id, statistics=['mean', 'median', 'mode'], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewer = viewer
        self.glue_data = data
        self.component_id = component_id
        self.statistics = statistics
        self.transform = kwargs.get("transform", None)
        self._bins = kwargs.get("bins", None)
        self._line = None
        if "color" in kwargs:
            self.color = kwargs["color"]
        if "unit" in kwargs:
            self.unit = kwargs["unit"]
        self.viewer.figure.observe(self._on_marks_updated, names=["marks"])

    def _mode(self):
        data = self.glue_data[self.component_id]
        if self.bins is not None:
            hist, bins = histogram(data, bins=self.bins)
            indices = flatnonzero(hist == amax(hist)) 
            return [0.5 * (bins[idx] + bins[idx + 1]) for idx in indices]
        else:
            counter = Counter(data)
            max_count = counter.most_common(1)[0][1]
            return [k for k, v in counter.items() if v == max_count]

    def _glue_statistic(self, stat):
        return self.glue_data.compute_statistic(stat, self.component_id)

    # glue doesn't implement a mode statistic, so we roll our own
    # Since there can be multiple modes, mode can be a list
    # and so we return a list for every statistic to make things simpler
    def _find_statistic(self, stat):
        if stat == 'mode':
            return self._mode()
        return [self._glue_statistic(stat)]

    @property
    def bins(self):
        if self._bins is not None:
            return self._bins
        if hasattr(self.viewer.state, "bins"):
            return self.viewer.state.bins
        return None

    # This is a bit of a hack to prevent layer artists from
    # redrawing their marks without ours included
    def _on_marks_updated(self, _marks):
        if self._line is not None and self._line not in self.viewer.figure.marks:
            self.viewer.figure.marks = self.viewer.figure.marks + [self._line]

    @observe('selected')
    def _update_marks(self, change):
        selected = change["new"]
        marks = [mark for mark in self.viewer.figure.marks if mark is not self._line]
        try:
            values = self._find_statistic(selected)
            if self.transform is not None:
                values = [self.transform(v) for v in values]
            for value in values:
                label = f"{selected.capitalize()}: {value}"
                if self.unit:
                    label += f" {self.unit}"
                line = vertical_line_mark(self.viewer.layers[0], value, self.color,
                                      label=label, label_visibility="none")
        except ValueError:
            line = None 

        self._line = line
        line_mark_list = [line] if line is not None else []
        self.viewer.figure.marks = marks + line_mark_list

