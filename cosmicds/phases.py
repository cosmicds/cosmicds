from glue_jupyter.state_traitlets_helpers import GlueState
from ipywidgets import widget_serialization
from traitlets import Dict, Unicode, default
from cosmicds.components.viewer_layout import ViewerLayout

from cosmicds.mixins import TemplateMixin, HubMixin
from cosmicds.utils import load_template
from glue.core import Data
from glue.core.state_objects import State
from echo import DictCallbackProperty, CallbackProperty, add_callback


class Story(State, HubMixin):
    name = CallbackProperty()
    stage_index = CallbackProperty(0)
    step_index = CallbackProperty(0)
    step_complete = CallbackProperty(False)
    stages = DictCallbackProperty()
    teacher_user = CallbackProperty()
    student_user = CallbackProperty()
    class_id = CallbackProperty()

    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._session = session

        # When the step index or completion status changes, store that change
        # in the stage state
        add_callback(self, 'step_index', self._on_step_index_changed)
        add_callback(self, 'step_complete', self._on_step_complete_changed)

    def _on_step_index_changed(self, value):
        self.stages[self.stage_index]['step_index'] = value
        self.step_complete = self.stages[self.stage_index]['steps'][
            self.step_index]['completed']

    def _on_step_complete_changed(self, value):
        self.stages[self.stage_index]['steps'][self.step_index][
            'completed'] = value


class Stage(TemplateMixin):
    template = Unicode().tag(sync=True)
    story_state = GlueState().tag(sync=True)
    stage_state = GlueState().tag(sync=True)
    app_state = GlueState().tag(sync=True)
    title = Unicode().tag(sync=True)
    subtitle = Unicode().tag(sync=True)
    viewers = Dict().tag(sync=True, **widget_serialization)
    widgets = Dict().tag(sync=True, **widget_serialization)

    def __init__(self, session, story_state, app_state, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._session = session
        self.story_state = story_state
        self.app_state = app_state

    def add_viewer(self, cls, label, data=None, layout=ViewerLayout, show_toolbar=True):
        viewer = self.app.new_data_viewer(cls, data=data, show=False)
        current_viewers = {k: v for k, v in self.viewers.items()}
        viewer_layout = layout(viewer)
        viewer_layout.show_toolbar = show_toolbar
        current_viewers.update({label: viewer_layout})
        self.viewers = current_viewers

        return viewer

    def add_widget(self, widget, label):
        current_widget = {k: v for k, v in self.widgets.items()}
        current_widget.update({label:widget})
        self.widgets = current_widget

    def get_viewer(self, label):
        return self.viewers[label].viewer

    def get_widget(self, label):
        return self.widgets[label]

    def set_viewer_attributes(self, viewer, dc_name, **kwargs):
        data = self.data_collection[dc_name]

        for k, v in kwargs.items():
            setattr(viewer.state, k, data.id[v])

    def add_link(self, from_dc_name, from_att, to_dc_name, to_att):
        from_dc = self.data_collection[from_dc_name]
        to_dc = self.data_collection[to_dc_name]

        self.app.add_link(from_dc, from_att, to_dc, to_att)

    def add_component(self, component, label):
        if self.components is None:
            self.components = {}

        current_components = {k: v for k, v in self.components.items()}
        current_components.update({label: component})
        self.components = current_components

    def get_component(self, label):
        return self.components[label]

    def add_data(self, data):
        self.data_collection.append(data)

    def get_data(self, dc_name):
        return self.data_collection[dc_name]

    def get_data_component(self, dc_name, id):
        data = self.data_collection[dc_name]
        return data.id[id]

    def update_data_value(self, dc_name, comp_name, value, index):
        data = self.data_collection[dc_name]
        values = data[comp_name]
        values[index] = value
        data.update_components({data.id[comp_name] : values})

    def add_data_values(self, dc_name, values):
        data = self.data_collection[dc_name]
        main_components = [x.label for x in data.main_components]
        component_dict = {c : list(data[c]) for c in main_components}
        for component, vals in component_dict.items():
            vals.append(values.get(component, None))
        new_data = Data(label=data.label, **component_dict)
        self.story_state.make_data_writeable(new_data)
        data.update_values_from_data(new_data)

    def vue_set_step_index(self, value):
        self.story_state.step_index = value

    def vue_set_step_complete(self, value):
        self.story_state.step_complete = value
