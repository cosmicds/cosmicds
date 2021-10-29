from glue.core import HubListener
from glue.core.data import Data
from glue.core.message import Message, SubsetMessage, SubsetCreateMessage, SubsetDeleteMessage
from glue.core.subset import Subset
from glue.core.subset_group import SubsetGroup, GroupedSubset

class SubsetModifierListener(HubListener):

    def __init__(self, app, source, modify, source_viewer_ids=[], modify_viewer_ids=[], listen=True, color=None):
        if isinstance(source, Data):
            self._source_data = source
            self._source = None
        elif isinstance(source, Subset) or isinstance(source, GroupedSubset):
            self._source = source
            self._source_data = source.data
        else:
            raise ValueError("Source must be Data, Subset, or GroupedSubset")
            
        self._app = app
        self._modify = modify
        self._modify_viewer_ids = modify_viewer_ids or list(app._viewer_handlers.keys())
        self._source_viewer_ids = source_viewer_ids or list(app._viewer_handlers.keys())
        self._color = color
        if listen:
            self.listen()

    def listen(self):
        self.hub.subscribe(self, SubsetMessage, handler=self._handle_message)

    def ignore(self):
        self.hub.unsubscribe(self, SubsetMessage)

    def clear_subset(self):
        if self._source is None:
            return

        data_collection = self._app.data_collection
        if isinstance(self._source, SubsetGroup):
            subset_group = self._source
            data_collection.remove_subset_group(subset_group)
        elif isinstance(self._source, GroupedSubset):
            subset_group = self._source.group
            data_collection.remove_subset_group(subset_group)
        elif isinstance(self._source, Subset):
            self._source.data.remove_subset(self._source)
        message = SubsetDeleteMessage(self._source, "subset_modifier_delete")
        self._handle_message(message)
        self._source = None

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

    def _create_mask(self, message):
        raise NotImplementedError("Listener has no _create_mask method")

    def _handle_message(self, message):

        # Do we care about this message?
        if not self._should_listen(message):
            return

        # If we don't have a source yet, it's the subset from this message
        if self._source is None and isinstance(message, SubsetCreateMessage):
            self._source = message.subset
            if self._color:
                message.subset.style.color = self._color

        # Get the subset mask and modify the subset
        subset_mask = self._create_mask(message)
        self._modify.subset_state = subset_mask
        self._modify.style.color = self._source.style.color

        # Since the subset created via the UI is really a SubsetGroup
        # the subset state gets broadcast to all of the data sets
        # In Qt glue, a viewer won't display this subset if it isn't based on
        # attributes linked to the viewer's data. But this doesn't seem to be the
        # case in glue-jupyter, so we handle this ourselves

        viewers = self._app._viewer_handlers.items()
        for key, viewer in viewers:
            if key not in self._source_viewer_ids:

                # We can't call remove_subset, since it's not the same subset in the other layer
                # It's just a member of the same subset group
                # But it will have the same label
                for layer in viewer.layers:
                    if layer.state.layer.label == self._source.label and layer.state.layer.data.label != self._source_data.label:
                        layer.state.visible = False
 
            # We also may want to control where the modified subset appears
            if key not in self._modify_viewer_ids:
                for layer in viewer.layers:
                    if layer.state.layer.label == self._modify.label:
                        layer.state.visible = False


    @property
    def source(self):
        return self._source

    @property
    def modify(self):
        return self._modify

    @property
    def hub(self):
        return self._app.data_collection.hub
