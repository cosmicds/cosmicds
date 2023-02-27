from glue.core.hub import Hub
from glue.core import SubsetGroup
import numpy as np
from glue.core.message import (DataCollectionAddMessage, DataCollectionDeleteMessage,
                              DataUpdateMessage, NumericalDataChangedMessage, SubsetUpdateMessage)
from glue.core import HubListener
from glue.core.subset import SubsetState
from ipyvuetify import VuetifyTemplate
from traitlets import Bool, Dict, List, Unicode, observe, HasTraits

from ...utils import convert_material_color, load_template

__all__ = ['Table']

_DEFAULT_TRANSFORM = lambda x: x

class Table(VuetifyTemplate, HubListener):
    default_color = 'dodgerblue'

    template = load_template("table.vue", __file__, traitlet=True).tag(sync=True)
    headers = List().tag(sync=True)
    items = List().tag(sync=True)
    key_component = Unicode().tag(sync=True)
    search = Unicode().tag(sync=True)
    single_select = Bool(False).tag(sync=True)
    selected = List().tag(sync=True)
    selected_class = Unicode("v-data-table__selected").tag(sync=True)
    sel_color = Unicode().tag(sync=True)
    sort_by = Unicode().tag(sync=True)
    title = Unicode().tag(sync=True)
    tools = Dict(default_value={}).tag(sync=True)
    use_search = Bool(False).tag(sync=True)

    def __init__(self, session, data, tools=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._session = session
        self.tool_functions = {}
        self._subset = kwargs.get('subset', None) # Can be either a subset or subset group
        self._is_subset_group = isinstance(self._subset, SubsetGroup)
        if self._subset is not None:
            self._subset_label = self._subset.label
        else:
            self._subset_label = kwargs.get("subset_label", "selected")

        # TODO - JC: At some point in the future, explore making
        # these regular glue tools
        if tools:
            for tool in tools:
                tool_id = tool["id"]
                self.tool_functions[tool_id] = tool["activate"]
                del tool["activate"]
                self.tools = {
                    tool_id: tool,
                    **self.tools
                }

        self.subset_color = kwargs.get('color', Table.default_color)
        self.use_subset_group = kwargs.get('use_subset_group', True)

        components = kwargs.get('glue_components', [x.label for x in data.components])
        self.key_component = kwargs.get('key_component', components[0])
        self.sort_by = self.key_component
        self._glue_data = data

        self.title = kwargs.get('title', '')
        self.selected_color = kwargs.get('selected_color', Table.default_color)

        self._glue_components = components
        self._glue_component_names = kwargs.get('names', components)
        self._data_collection_delete_filter = lambda message: message.data == self._glue_data
        self._data_update_filter = lambda message: message.data == self._glue_data and message.attribute in self._glue_components
        self._data_changed_filter = lambda message: message.data == self._glue_data
        self._transforms = kwargs.get('transforms', {})

        def subset_changed_filter(message):
            if self._is_subset_group:
                return message.subset in self._subset.subsets and message.subset.data == self._glue_data
            else:
                return message.subset == self._subset
        self._subset_changed_filter = subset_changed_filter
        self.single_select = kwargs.get('single_select', False)
        self._on_create_subset = kwargs.get("on_create_subset", None)

        self._subset_message_pass = False

        self._row_click_callback = None

        # Populate the table with the current data in the collection
        self._populate_table()

        # Subscribe to change events to update the table accordingly
        self.hub.subscribe(self, DataCollectionDeleteMessage,
                           handler=self._on_data_collection_delete, filter=self._data_collection_delete_filter)
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
    def subset(self):
        return self._subset

    @property
    def subset_label(self):
        return self._subset_label

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

    @subset.setter
    def subset(self, subset):
        self._subset = subset
        self._subset_label = subset.label
        self._is_subset_group = isinstance(self._subset, SubsetGroup)
        self.selected = self._selection_from_state(self._subset.subset_state)

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

    def _transform(self, component):
        return self._transforms.get(component, _DEFAULT_TRANSFORM)

    def _populate_table(self):
        df = self._glue_data.to_dataframe()
        self.headers = [{
            'text':  name,
            'value': component
        } for name, component in zip(self._glue_component_names, self._glue_components)]
        self.headers[0]['align'] = 'start'
        self.items = [
            {
                component : self._transform(component)(getattr(row, component, None)) for component in self._glue_components
            } for row in df.itertuples()
        ]

    def _new_subset(self):
        state = self.subset_state_from_selected(self.selected)
        if self.use_subset_group:
            subset = self.data_collection.new_subset_group(label=self._subset_label, subset_state=state, color=self.subset_color)
        else:
            subset = self._glue_data.new_subset(label=self._subset_label, subset=state, color=self.subset_color)
        if self._on_create_subset is not None:
            self._on_create_subset(subset)
        return subset

    def _on_data_updated(self, message=None):
        self._populate_table()

    def _on_subset_updated(self, message=None):
        if self._subset_message_pass:
            self._subset_message_pass = False
            return

        if self._subset is not None:
            self.selected = self._selection_from_state(self._subset.subset_state)

    def _on_data_deleted(self):
        self.data_collection.remove_subset_group(self._subset)
        self.subset = None
        self.items = {}

    def _on_data_collection_delete(self, message=None):
        self._on_data_deleted()

    def update_subset(self, selected):
        if self.subset is None:
            self.subset = self._new_subset()
        else:
            state = self.subset_state_from_selected(selected)
            self._subset_message_pass = True
            self._subset.subset_state = state

    @observe('selected')
    def _on_selected_changed(self, event):
        self.update_subset(event["new"])

    @property
    def selected_keys(self):
        return [item[self.key_component] for item in self.selected]

    def initialize_subset_if_needed(self):
        if self._subset is None:
            self.subset = self._new_subset()
            
    def indices_from_items(self, items):
        state = self.subset_state_from_selected(items)
        mask = state.to_mask(self.glue_data)
        return [index for index in range(len(mask)) if mask[index]]

    @property
    def indices(self):
        return self.indices_from_items(self.selected)

    @property
    def index(self):
        if self.single_select and len(self.indices) > 0:
            return self.indices[0]
        return None

    @property
    def row_click_callback(self):
        return self._row_click_callback

    @row_click_callback.setter
    def row_click_callback(self, cb):
        self._row_click_callback = cb

    def vue_handle_row_click(self, item, data=None):
        key = item[self.key_component]
        if self.row_click_callback:
            self.row_click_callback(item, data)
        if self.single_select:
            self.selected = [item]

        # We can't just use append/remove here
        # We need a reassignment so that the watcher is triggered
        elif key in self.selected_keys:
            self.selected = [x for x in self.selected if x[self.key_component] != key]
        else:
            self.selected = self.selected + [item]

    def vue_update_sort_by(self, field, _args=None):
        # We get a list of the form ['sort_field']
        # which is empty is there isn't a sort field selected
        # We default to the key component
        self.sort_by = field[0] if len(field) > 0 else self.key_component

    def update_tool(self, tool):
        self.send({"method": "update_tool", "args": [tool]})

    def get_tool(self, tool_id):
        return self.tools[tool_id]
        
    def vue_activate_tool(self, tool_id):
        tool = self.get_tool(tool_id)
        func = self.tool_functions.get(tool_id, None)
        if tool and func:
            func(self, tool)
            self.update_tool(tool)
            
