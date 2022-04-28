from glue.core.message import SubsetDeleteMessage
from glue.core.subset import MultiRangeSubsetState
from itertools import groupby
from numpy import array, isin, unique

from cosmicds.tools.line_fit_tool import LineFitTool

from .subset_modifier_listener import SubsetModifierListener
class HistogramListener(SubsetModifierListener):

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

        print("Subset state!")
        print(subset_state)

        return subset_state
