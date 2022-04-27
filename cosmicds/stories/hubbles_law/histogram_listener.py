from glue.core.message import SubsetDeleteMessage
from glue.core.subset import MultiRangeSubsetState
from itertools import groupby
from numpy import array, isin, unique

from cosmicds.tools.line_fit_tool import LineFitTool

from .subset_modifier_listener import SubsetModifierListener
class HistogramListener(SubsetModifierListener):

    def __init__(self, state, source_sg, source_data, modify_sg, modify_data, scatter_viewer_id, listen=False, color=None):
        super().__init__(state, source_sg, source_data, modify_sg, modify_data, listen=listen, color=color)
        self.scatter_viewer_id = scatter_viewer_id

    @property
    def scatter_viewer(self):
        return self._state.get_viewer(self.scatter_viewer_id)

    def _ranges(self, ids):
        rgs = []
        for _, b in groupby(enumerate(ids), lambda pair: pair[1] - pair[0]):
            b = list(b)
            rgs.append((b[0][1], b[-1][1]))
        return rgs

    def _create_subset_state(self, message):
        # Get the student IDs present in the selected
        # histogram bar(s)
        subset = message.subset
        student_ids = list(unique(subset['student_id']))
        id_ranges = self._ranges(student_ids)
        component = self._modify_data.id['student_id']
        subset_state = MultiRangeSubsetState(id_ranges, component)
        self._current_ids = student_ids

        return subset_state
