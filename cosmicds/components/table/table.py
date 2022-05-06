from glue.core.hub import Hub
import numpy as np
from glue.core.message import (DataCollectionAddMessage,
                               DataCollectionDeleteMessage, DataUpdateMessage, NumericalDataChangedMessage, SubsetUpdateMessage)
from glue.core import HubListener
from glue.core.subset import SubsetState
from ipyvuetify import VuetifyTemplate
from traitlets import Bool, List, Unicode, observe

from ...utils import convert_material_color, load_template

__all__ = ['Table']


class Table(VuetifyTemplate, HubListener):
    default_color = 'dodgerblue'

    template = load_template("table.vue", __file__, traitlet=True).tag(sync=True)
    headers = List().tag(sync=True)
    items = List().tag(sync=True)
    key_component = Unicode().tag(sync=True)
    search = Unicode().tag(sync=True)
    single_select = Bool(False).tag(sync=True)
    selected = List().tag(sync=True)
    sel_color = Unicode().tag(sync=True)
    sort_by = Unicode().tag(sync=True)
    title = Unicode().tag(sync=True)
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
        self.sort_by = self.key_component
        self._glue_data = data

        self.title = kwargs.get('title', '')
        self.selected_color = kwargs.get('selected_color', Table.default_color)

        self._glue_components = components
        self._glue_component_names = kwargs.get('names', components)
        self._data_update_filter = lambda message: message.data.label == self._glue_data.label and message.attribute in self._glue_components
        self._data_changed_filter = lambda message: message.data.label == self._glue_data.label
        #self._data_changed_filter = lambda _: True
        def subset_changed_filter(message):
            #print("Got a message")
            #print(message.subset.label)
            return message.subset.label == self._subset_group_label and message.subset.data.label == self._glue_data.label
        self._subset_changed_filter = subset_changed_filter
        #self._subset_changed_filter = lambda message: message.subset.label == self._subset_group_label and message.subset.data.label == self._glue_data.label

        self.single_select = kwargs.get('single_select', False)

        self._subset_message_pass = False

        self._row_click_callback = None

        # Populate the table with the current data in the collection
        self._populate_table()

        # Subscribe to change events that alter the data collection so that
        # the table can be updated accordingly
        self.hub.subscribe(self, DataCollectionAddMessage,
                           handler=self._on_data_collection_updated)
        self.hub.subscribe(self, DataCollectionDeleteMessage,
                           handler=self._on_data_collection_updated)
        self.hub.subscribe(self, DataUpdateMessage,
                           handler=self._on_data_updated, filter=self._data_update_filter)
        self.hub.subscribe(self, NumericalDataChangedMessage,
                           handler=self._on_data_updated, filter=self._data_changed_filter)
        self.hub.subscribe(self, SubsetUpdateMessage,
                           handler=self._on_subset_updated, filter=self._subset_changed_filter)

    @property
    def data_collection(self):
        return self._session.data_collection

    @property
    def hub(self):
        return self._session.hub

    @property
    def glue_data(self):
        return self._glue_data

    @property
    def subset_group(self):
        return self._subset_group

    @property
    def selected_color(self):
        return self.sel_color

    @selected_color.setter
    def selected_color(self, value):
        if value.startswith("colors"):
            value = convert_material_color(value)
        self.sel_color = value

    @glue_data.setter
    def glue_data(self, data):
        self._glue_data = data
        self._populate_table()

    @subset_group.setter
    def subset_group(self, group):
        self._subset_group = group
        self._subset_group_label = group.label
        self.selected = self._selection_from_state(self._subset_group.subset_state)

    def subset_state_from_selected(self, selected):
        keys = [x[self.key_component] for x in selected]
        if keys:
            state = np.bitwise_or.reduce([self._glue_data.id[self.key_component] == x for x in keys])
        else:
            state = SubsetState()
        return state

    def _selection_from_state(self, state):
        mask = state.to_mask(self._glue_data)
        return [item for index, item in enumerate(self.items) if mask[index]]

    def _populate_table(self):
        df = self._glue_data.to_dataframe()
        self.headers = [{
            'text': self._glue_component_names[index],
            'value': self._glue_components[index]
        } for index in range(len(self._glue_components))]
        self.headers[0]['align'] = 'start'
        self.items = [
            {
                component : getattr(row, component, None) for component in self._glue_components
            } for row in df.itertuples()
        ]

    def _on_data_added(self):
        self._glue_data = self.data_collection[self._glue_data.label]
        state = self.subset_state_from_selected(self.selected)
        self._subset_group = self.data_collection.new_subset_group(self._subset_group_label, state)
        self._subset_group.style.color = self.selected_color

    def _on_data_updated(self, message=None):
        self._populate_table()

    def _on_subset_updated(self, message=None):
        if self._subset_message_pass:
            self._subset_message_pass = False
            return

        if self._subset_group is not None:
            self.selected = self._selection_from_state(self._subset_group.subset_state)

    def _on_data_deleted(self):
        self.data_collection.remove_subset_group(self._subset_group)
        self._subset_group = None

    def _on_data_collection_updated(self, message=None):
        if message is not None and message.data.label == self._glue_data.label:
            if isinstance(message, DataCollectionAddMessage):
                self._on_data_added()
            else:
                self._on_data_deleted()
        self._populate_table()
        

    @observe('selected')
    def _on_selected_changed(self, event):
        state = self.subset_state_from_selected(event['new'])
        if self._subset_group is None:
            self._subset_group = self.data_collection.new_subset_group(self._subset_group_label, state)
        else:
            self._subset_message_pass = True
            self._subset_group.subset_state = state
            
    def indices_from_items(self, items):
        state = self.subset_state_from_selected(items)
        mask = state.to_mask(self.glue_data)
        return [index for index in range(len(mask)) if mask[index]]

    @property
    def indices(self):
        return self.indices_from_items(self.selected)

    @property
    def index(self):
        if self.single_select:
            return self.indices[0]
        return None

    @property
    def row_click_callback(self):
        return self._row_click_callback

    @row_click_callback.setter
    def row_click_callback(self, cb):
        self._row_click_callback = cb

    def vue_handle_row_click(self, item, data=None):
        if self.row_click_callback:
            self.row_click_callback(item, data)
        if self.single_select:
            self.selected = [item]

        # We can't just use append/remove here
        # We need a reassignment so that the watcher is triggered
        elif item in self.selected:
            self.selected = [x for x in self.selected if x != item]
        else:
            self.selected = self.selected + [item]

    def vue_update_sort_by(self, field, _args=None):
        self.sort_by = field
