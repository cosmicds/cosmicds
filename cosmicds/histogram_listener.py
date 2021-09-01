from glue.core import Hub, HubListener, Data, DataCollection, data_collection, subset
from glue.core.message import SubsetMessage, SubsetCreateMessage, SubsetDeleteMessage, SubsetUpdateMessage
from glue.core.subset import MaskSubsetState

from numpy import isin, unique

class HistogramListener(HubListener):

    def __init__(self, app, modify, source_data):
        self._source_data = source_data
        self._source = None
        self._modify = modify
        self._app = app
        self._hub = app.data_collection.hub
        self._hub.subscribe(self, SubsetMessage, handler=self.handle_message)

    def _should_listen(self, message):
        """
        This method checks that a message is of the right type (SubsetMessage)
        and that it was sent by the subset that we care about
        """
        if not isinstance(message, SubsetMessage):
            return False
        
        if self._source is None:
            return message.subset.data.uuid == self._source_data.uuid
        else:
            return message.subset == self._source
        
    def handle_message(self, message):

        # Do we care about this message?
        if not self._should_listen(message):
            return

        # If we do, get the student IDs present in the selected
        # histogram bar(s)
        subset = message.subset
        self._source = self._source or subset
        student_ids = list(unique(subset['student_id']))

        data = self._modify.data
        subset_mask = isin(data['student_id'], student_ids)
        self._modify.subset_state = subset_mask
        viewer = self._app._viewer_handlers['hub_students_viewer']
        for layer in viewer.layers:
            if layer.state.layer.label == self._source.label:
                layer.state.visible = False
         