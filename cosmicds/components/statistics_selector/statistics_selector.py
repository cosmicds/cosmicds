from ipyvuetify import VuetifyTemplate
from traitlets import List, observe

from ...utils import load_template, vertical_line_mark

class StatisticsSelector(VuetifyTemplate):

    template = load_template("statistics_selector.vue", __file__, traitlet=True).tag(sync=True)
    selected = List().tag(sync=True)
    statistics = List().tag(sync=True)
    colors = List(['red', 'orange', 'yellow', 'green', 'blue', 'purple']).tag(sync=True)

    def __init__(self, viewer, data, component_id, layer, statistics=['mean', 'median', 'mode'], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewer = viewer
        self.data = data
        self.component_id = component_id
        self.layer = layer
        self.statistics = statistics
        self._lines = []

    @observe('selected')
    def _update_marks(self, change):
        selected = change["new"]
        marks = [mark for mark in self.viewer.figure.marks if mark not in self._lines]
        lines = []
        for index, stat in enumerate(selected):
            try:
                value = self.data.compute_statistic(stat, self.component_id)
                mark = vertical_line_mark(self.layer, value, self.colors[index])
                lines.append(mark)
            except ValueError:
                continue

        self.viewer.figure.marks = marks + lines
        self._lines = lines

