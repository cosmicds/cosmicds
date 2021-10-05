from glue.core.hub import Hub
import numpy as np
from glue.core.message import (DataCollectionAddMessage,
                               DataCollectionDeleteMessage, DataUpdateMessage)
from glue.core import HubListener
from glue.core.subset import SubsetState
from ipyvuetify import VuetifyTemplate
from traitlets import Bool, List, Unicode

from ...utils import load_template

__all__ = ['Table']


class Table(VuetifyTemplate, HubListener):
    default_color = '#00ff00'

    template = load_template("table.vue", __file__).tag(sync=True)
    headers = List().tag(sync=True)
    items = List().tag(sync=True)
    key_component = Unicode().tag(sync=True)
    search = Unicode().tag(sync=True)
    single_select = Bool(False).tag(sync=True)
    selected = List().tag(sync=True)
    use_search = Bool(False).tag(sync=True)

    def __init__(self, session, data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._session = session
        self._subset_group = kwargs.get('subset_group', None)
        if self._subset_group is not None:
            self._subset_group_label = self._subset_group.label
        else:
            self._subset_group_label = "selected"

        components = kwargs.get('glue_components', [x.label for x in data.components])
        self.key_component = kwargs.get('key_component', components[0])
        self.glue_data = data
        self._data_label = data.label

        self.glue_components = components
        self.glue_component_names = kwargs.get('names', components)
        self._message_filter = lambda message: message.attribute in self.glue_components

        self.single_select = kwargs.get('single_select', False)
        self.subset_color = kwargs.get('color', Table.default_color)

        # Populate the table with the current data in the collection
        self._populate_table()

        # Subscribe to change events that alter the data collection so that
        # the table can be updated accordingly
        self.hub.subscribe(self, DataCollectionAddMessage,
                           handler=self._on_data_collection_updated)
        self.hub.subscribe(self, DataCollectionDeleteMessage,
                           handler=self._on_data_collection_updated)
        self.hub.subscribe(self, DataUpdateMessage,
                           handler=self._on_data_updated, filter=self._message_filter)

        # Listen for changes to selected rows
        self.observe(self._on_selected_changed, names=['selected'])

    @property
    def data_collection(self):
        return self._session.data_collection

    @property
    def hub(self):
        return self._session.hub

    def _subset_state_from_selected(self, selected):
        keys = [x[self.key_component] for x in selected]
        if keys:
            state = np.bitwise_or.reduce([self.glue_data.id[self.key_component] == x for x in keys])
        else:
            state = SubsetState()
        return state

    def _selection_from_state(self, state):
        mask = state.to_mask(self.glue_data)
        return [item for index, item in enumerate(self.items) if mask[index]]

    def _populate_table(self):
        df = self.glue_data.to_dataframe()
        self.headers = [{
            'text': self.glue_component_names[index],
            'value': self.glue_components[index]
        } for index in range(len(self.glue_components))]
        self.headers[0]['align'] = 'start'
        self.items = [
            {
                component : getattr(row, component, None) for component in self.glue_components
            } for row in df.itertuples()
        ]

    def _on_data_added(self):
        self.glue_data = self.data_collection[self._data_label]
        state = self._subset_state_from_selected(self.selected)
        self._subset_group = self.data_collection.new_subset_group(self._subset_group_label, state)
        self._subset_group.style.color = self.subset_color

    def _on_data_updated(self, message=None):
        if self._subset_group is not None:
            self.selected = self._selection_from_state(self._subset_group.subset_state)
            self._populate_table()

    def _on_data_deleted(self):
        self.data_collection.remove_subset_group(self._subset_group)
        self._subset_group = None

    def _on_data_collection_updated(self, message=None):

        # print("Table received a message:")
        # print(type(message))
        # print(message.data.label)

        # print("Is this message about our data?")
        # print(message.data.label == self._data_label)

        if message is not None and message.data.label == self._data_label:
            if isinstance(message, DataCollectionAddMessage):
                self._on_data_added()
            else:
                self._on_data_deleted()
        self._populate_table()
        
    def _on_selected_changed(self, _event):
        state = self._subset_state_from_selected(_event['new'])
        if self._subset_group is None:
            self._subset_group = self.data_collection.new_subset_group(self._subset_group_label, state)
        else:
            self._subset_group.state = state

