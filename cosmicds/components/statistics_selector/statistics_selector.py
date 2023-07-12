from collections import Counter
from ipyvuetify import VuetifyTemplate
from numpy import argmax, histogram
from traitlets import List, Unicode, observe

from ...utils import load_template, vertical_line_mark

class StatisticsSelector(VuetifyTemplate):

    template = load_template("statistics_selector.vue", __file__, traitlet=True).tag(sync=True)
    selected = List().tag(sync=True)
    statistics = List().tag(sync=True)
    colors = List(['red', 'orange', 'yellow', 'green', 'blue', 'purple']).tag(sync=True)
    unit = Unicode().tag(sync=True)

    def __init__(self, viewer, data, component_id, statistics=['mean', 'median', 'mode'], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewer = viewer
        self.glue_data = data
        self.component_id = component_id
        self.statistics = statistics
        self.transform = kwargs.get("transform", None)
        self._bins = kwargs.get("bins", None)
        if "colors" in kwargs:
            self.colors = kwargs["colors"]
        if "unit" in kwargs:
            self.unit = kwargs["unit"]
        self._lines = []

    def _mode(self):
        data = self.glue_data[self.component_id]
        if self.bins is not None:
            hist, bins = histogram(data, bins=self.bins)
            idx = argmax(hist)
            return 0.5 * (bins[idx] + bins[idx + 1])
        else:
            counter = Counter(data)
            return counter.most_common(1)[0]

    def _glue_statistic(self, stat):
        return self.glue_data.compute_statistic(stat, self.component_id)

    # glue doesn't implement a mode statistic, so we roll our own
    def _find_statistic(self, stat):
        if stat == 'mode':
            return self._mode()
        return self._glue_statistic(stat)

    @property
    def bins(self):
        if self._bins is not None:
            return self._bins
        if hasattr(self.viewer.state, "bins"):
            return self.viewer.state.bins
        return None

    @observe('selected')
    def _update_marks(self, change):
        selected = change["new"]
        marks = [mark for mark in self.viewer.figure.marks if mark not in self._lines]
        lines = []
        for index, stat in enumerate(self.statistics):
            if stat not in selected:
               continue 
            try:
                value = self._find_statistic(stat)
                if self.transform is not None:
                    value = self.transform(value)
                label = f"{stat.capitalize()}: {value}"
                if self.unit:
                    label += f" {self.unit}"
                mark = vertical_line_mark(self.viewer.layers[0], value, self.colors[index],
                                          label=label, label_visibility="none")
                lines.append(mark)
            except ValueError:
                continue

        self.viewer.figure.marks = marks + lines
        self._lines = lines

