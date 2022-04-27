from glue.core import HubListener
from glue.core.data import Data
from glue.core.message import Message, SubsetMessage
from glue.core.subset import Subset, SubsetState
from glue.core.subset_group import SubsetGroup, GroupedSubset

class SubsetModifierListener(HubListener):

    def __init__(self, state, source_sg, source_data, modify_sg, modify_data, listen=False, color=None):
            
        self._state = state
        self._source_sg = source_sg
        self._modify_sg = modify_sg
        self._source_data = source_data
        self._modify_data = modify_data
        self._color = color

        if listen:
            self.listen()

    def listen(self):
        self.hub.subscribe(self, SubsetMessage, handler=self._handle_message)

    def ignore(self):
        self.hub.unsubscribe(self, SubsetMessage)

    def clear_subset(self):
        self._source_sg.subset_state = SubsetState()
        self._modify_sg.subset_state = SubsetState()

    def _should_listen(self, message):
        """
        This method checks that a message is of the right type (SubsetMessage)
        and that it was sent by the subset that we care about
        """
        if not isinstance(message, SubsetMessage):
            return False
        
        return message.subset in self._source_sg.subsets and message.subset.data.label == self._source_data.label

    def _create_subset_state(self, message):
        raise NotImplementedError("Listener has no _create_subset_state method")

    def _handle_message(self, message):

        # Do we care about this message?
        if not self._should_listen(message):
            return

        # Get the subset mask and modify the subset
        subset_state = self._create_subset_state(message)
        self._modify_sg.subset_state = subset_state


    @property
    def source(self):
        return self._source_data

    @property
    def modify(self):
        return self._modify_data

    @property
    def hub(self):
        return self._state.data_collection.hub

    @property
    def source_group(self):
        return self._source_sg

    @property
    def modify_group(self):
        return self._modify_sg
