from echo import delay_callback, ignore_callback
from echo.callback_container import CallbackContainer
from glue.viewers.common.layer_artist import LayerArtist
from ipyvuetify import VuetifyTemplate
from traitlets import List, observe

from ...utils import load_template

class LayerToggle(VuetifyTemplate):

    template = load_template("layer_toggle.vue", __file__, traitlet=True).tag(sync=True)
    layers = List().tag(sync=True)
    selected = List().tag(sync=True)

    def __init__(self, viewer, names=None, sort=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewer = viewer
        self.name_transform = LayerToggle._create_name_transform(names)
        self.sort = sort or (lambda state: state.zorder)

        self._ignore_conditions = CallbackContainer()

        self._update_from_viewer()
        self.viewer.state.add_callback('layers', self._update_from_viewer)

    def _ignore_layer(self, layer):
        for cb in self._ignore_conditions:
            if cb(layer):
                return True
        return False

    def _layer_data(self, state):
        return {
            "color": state.color,
            "label": self.name_transform(state.layer.label)
        }

    def _layer_index(self, layers, layer):
        try:
            index = layers.index(layer)
            return index
        except ValueError:
            return len(layers) + 1

    def set_layer_order(self, layers):
        def sort_key(layer):
            if isinstance(layer, LayerArtist):
                layer = layer.state
            return (self._layer_index(layers, layer), layer.zorder)
        self.sort_by(sort_key)

    def sort_by(self, sort):
        self.sort = sort
        self._update_from_viewer()  

    def watched_layer_states(self, layers=None):
        layers = layers or self.viewer.state.layers
        return sorted([state for state in layers if not self._ignore_layer(state)], key=self.sort)

    def add_ignore_condition(self, condition):
        self._ignore_conditions.append(condition)
        self._update_from_viewer()

    def remove_ignore_condition(self, condition):
        self._ignore_conditions.remove(condition)
        self._update_from_viewer()

    def _update_from_viewer(self, layers=None):
        watched = self.watched_layer_states(layers)
        self.layers = [self._layer_data(state) for state in watched]
        self.selected = [index for index, state in enumerate(watched) if state.visible]

    @observe('selected')
    def _on_selected_change(self, change):
        selected = change["new"]
        with delay_callback(self.viewer.state, 'layers'):
            for index, state in enumerate(self.watched_layer_states()):
                if not self._ignore_layer(state):
                    state.visible = index in selected

    @staticmethod
    def _create_name_transform(namer):
        if callable(namer):
            return namer
        elif isinstance(namer, dict):
            def transform(label):
                name = namer.get(label, label)
                return name or LayerToggle._default_transform(label)
            return transform
        else:
            return LayerToggle._default_transform

    @staticmethod
    def _default_transform(label):
        return label
