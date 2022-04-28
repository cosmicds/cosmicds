from glue.core import HubListener
from glue.core.data import Data
from glue.core.message import Message, SubsetMessage
from glue.core.subset import Subset, SubsetState
from glue.core.subset_group import SubsetGroup, GroupedSubset

class SubsetModifierListener(HubListener):

    def __init__(self, state, source_subset, source_data, modify_subset, modify_data, **kwargs):
        
        # Source and modify subsets can be either subsets or subset groups
        self._state = state
        self._source_subset = source_subset
        self._modify_subset = modify_subset
        self._source_data = source_data
        self._modify_data = modify_data
        self._color = kwargs.get("color", None)
        self._use_group = kwargs.get("use_group", True)
        self._before_create_subset = kwargs.get("before_create_modify_subset", None)
        self._modify_subset_label = kwargs.get("modify_subset_label", "modify_subset") if self._modify_subset is None else self._modify_subset.label

        if kwargs.get("listen", False):
            self.listen()

    def listen(self):
        self.hub.subscribe(self, SubsetMessage, handler=self._handle_message)

    def ignore(self):
        self.hub.unsubscribe(self, SubsetMessage)

    def clear_subset(self):
        self._source_subset.subset_state = SubsetState()
        self._modify_subset.subset_state = SubsetState()

    def _should_listen(self, message):
        """
        This method checks that a message is of the right type (SubsetMessage)
        and that it was sent by the subset that we care about
        """
        if not isinstance(message, SubsetMessage):
            return False

        if message.subset.data.label == self._source_data.label:
            return (self._source_subset is None) or (message.subset in self._source_subset.subsets)

        return False

    def _create_subset_state(self, message):
        raise NotImplementedError("Listener has no _create_subset_state method")

    def _create_modify_subset(self, state):
        if self._use_group:
            subset = self.data_collection.new_subset_group(label=self._modify_subset_label, subset_state=state, color=self.modify.state.color)
        else:
            subset = self.modify.new_subset(label=self._modify_subset_label, state=state, color=self.modify.state.color)
        return subset


    def _handle_message(self, message):

        # Do we care about this message?
        if not self._should_listen(message):
            return

        # Get the subset mask and modify the subset
        subset_state = self._create_subset_state(message)
        if self._modify_subset is None:
            print(self._before_create_subset)
            if self._before_create_subset is not None:
                self._before_create_subset(self._modify_subset_label)
            self._modify_subset = self._create_modify_subset(subset_state)
        else:
            self._modify_subset.subset_state = subset_state


    @property
    def source(self):
        return self._source_data

    @property
    def modify(self):
        return self._modify_data

    @property
    def data_collection(self):
        return self._state.data_collection

    @property
    def hub(self):
        return self.data_collection.hub

    @property
    def source_subset(self):
        return self._source_subset

    @source_subset.setter
    def source_subset(self, value):
        self._source_subset = value

    @property
    def modify_group(self):
        return self._modify_subset
