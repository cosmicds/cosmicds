from glue.core.message import SubsetDeleteMessage
from numpy import array, isin, unique

from .subset_modifier_listener import SubsetModifierListener
class HistogramListener(SubsetModifierListener):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def _handle_message(self, message):

        super()._handle_message(message)

        # Add a fit line if the subset has a nonzero number of data points
        # Otherwise, clear lines
        if self._modify.size > 0:
            viewer = self._app._viewer_handlers['hub_students_viewer']
            layer_index = -1
            for index, layer in enumerate(viewer.layers):
                if layer.state.layer.label == self._modify.label:
                    layer_index = index
            
            if layer_index < 0:
                return

            self._app.vue_fit_lines({
                'viewer_id': 'hub_students_viewer',
                'layers': [layer_index],
                'clear_others': True,
                'aggregate': False
            })

        else:
            self._app.vue_clear_lines('hub_students_viewer')
