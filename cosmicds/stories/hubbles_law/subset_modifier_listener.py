from glue.core import HubListener
from glue.core.message import SubsetMessage
from glue.core.subset import SubsetState
from glue.core.subset_group import SubsetGroup

class SubsetModifierListener(HubListener):

    def __init__(self, state, source_subset, source_data, modify_subset, modify_data, **kwargs):
        
        # Source and modify subsets can be either subsets or subset groups
        self._state = state
        self._source_subset = source_subset
        self._is_source_group = isinstance(source_subset, SubsetGroup)
        self._modify_subset = modify_subset
        self._source_data = source_data
        self._modify_data = modify_data
        self._color = kwargs.get("color", None)
        self._use_group = kwargs.get("use_group", True)
        self._source_subset_label = kwargs.get("source_subset_label", "source_subset") if self._source_subset is None else self._source_subset.albel
        self._modify_subset_label = kwargs.get("modify_subset_label", "modify_subset") if self._modify_subset is None else self._modify_subset.label

        if kwargs.get("listen", True):
            self.listen()

    def listen(self):
        self.hub.subscribe(self, SubsetMessage, handler=self._handle_message, filter=self._should_listen)

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

        if (self._source_subset is None or \
            not isinstance(message, SubsetMessage) or \
            message.subset.data != self._source_data):
            return False

        if message.subset.data == self._source_data:
            if self._is_source_group:
                listen = message.subset in self._source_subset.subsets
            else:
                listen = message.subset == self._source_subset

        return listen

    def _create_subset_state(self, message):
        raise NotImplementedError("Listener has no _create_subset_state method")

    def _create_modify_subset(self, state):
        if self._use_group:
            # PR coming soon to add more visual attributes in the subset group constructor
            subset = self.data_collection.new_subset_group(label=self._modify_subset_label, subset_state=state)
            subset.style.color = self.modify_data.style.color
        else:
            subset = self.modify_data.new_subset(label=self._modify_subset_label, state=state, color=self.modify_data.state.color)
        return subset


    def _handle_message(self, message):
        self._update_modify(message.subset)

    def _update_modify(self, subset):

        # Get the subset state and modify the subset
        subset_state = self._create_subset_state(subset)
        if self._modify_subset is None:
            self._modify_subset = self._create_modify_subset(subset_state)
        else:
            self._modify_subset.subset_state = subset_state


    @property
    def source_data(self):
        return self._source_data

    @property
    def modify_data(self):
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

    @property
    def source_subset_label(self):
        return self._source_subset_label

    @source_subset.setter
    def source_subset(self, value):
        self._source_subset = value
        self._source_subset_label = value.label
        self._is_source_group = isinstance(value, SubsetGroup)
        if self._is_source_group:
            subset = next(x for x in value.subsets if x.data == self._source_data)
        else:
            subset = value
        self._update_modify(subset)


    @property
    def modify_subset(self):
        return self._modify_subset
