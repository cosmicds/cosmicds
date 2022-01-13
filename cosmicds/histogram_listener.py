from glue.core.message import SubsetDeleteMessage
from glue.core.subset import MultiRangeSubsetState
from itertools import groupby
from numpy import array, isin, unique

from .subset_modifier_listener import SubsetModifierListener
class HistogramListener(SubsetModifierListener):

    def _ranges(self, ids):
        rgs = []
        for a, b in groupby(enumerate(ids), lambda pair: pair[1] - pair[0]):
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

    def clear_subset(self):
        super().clear_subset()
        
        viewer_id = 'hub_comparison_viewer'
        layer_index = self._layer_index()
        if layer_index >= 0:
            self._app.vue_clear_lines(viewer_id, [layer_index])

    def _layer_index(self):
        layer_index = -1
        viewer_id = 'hub_comparison_viewer'
        viewer = self._app._viewer_handlers[viewer_id]
        for index, layer in enumerate(viewer.layers):
            if layer.state.layer.label == self._modify_sg.label and layer.state.layer.data.label == self._modify_data.label:
                layer_index = index
                break
        return layer_index

    def _handle_message(self, message):

        if not self._should_listen(message):
            return

        super()._handle_message(message)

        # Add a fit line if the subset has a nonzero number of data points
        # Otherwise, clear lines
        
        viewer_id = 'hub_comparison_viewer'
        viewer = self._app._viewer_handlers[viewer_id]
        layer_index = self._layer_index()
        
        if layer_index < 0:
            return

        if message.subset.size > 0:
            self._app.vue_fit_lines({
                'viewer_id': viewer_id,
                'layers': [layer_index],
                'clear_others': False,
                'aggregate': False
            })

        else:
            self._app.vue_clear_lines(viewer_id, [layer_index])