from glue.core.message import SubsetDeleteMessage
from numpy import array, isin, unique

from .subset_modifier_listener import SubsetModifierListener
class HistogramListener(SubsetModifierListener):

    def __init__(self, app, source, modify, source_viewer_ids=[], modify_viewer_ids=[], listen=True):
        super().__init__(app, source, modify, source_viewer_ids, modify_viewer_ids, listen)

    def _create_mask(self, message):

        # Handle delete messages slightly differently
        subset = message.subset
        if isinstance(message, SubsetDeleteMessage):
            return array([False] * self._modify.size)

        # If we do, get the student IDs present in the selected
        # histogram bar(s)
        student_ids = list(unique(subset['student_id']))
        subset_mask = isin(self._modify.data['student_id'], student_ids)

        return subset_mask

