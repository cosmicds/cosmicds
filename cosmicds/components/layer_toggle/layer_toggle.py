from echo import delay_callback
from ipyvuetify import VuetifyTemplate
from traitlets import List, observe

from ...utils import load_template

class LayerToggle(VuetifyTemplate):

    template = load_template("layer_toggle.vue", __file__, traitlet=True).tag(sync=True)
    layers = List().tag(sync=True)
    selected = List().tag(sync=True)

    def __init__(self, viewer, names=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewer = viewer
        self.name_transform = LayerToggle._create_name_transform(names)

        self._update_layers_from_viewer()
        self.viewer.state.add_callback('layers', self._update_layers_from_viewer)

    def _layer_data(self, layer):
        return {
            "color": layer.state.color,
            "label": self.name_transform(layer.layer.label)
        }

    def _update_layers_from_viewer(self, layers=None):
        self.layers = [self._layer_data(layer) for layer in self.viewer.layers]
        self.selected = [index for index, layer in enumerate(self.viewer.layers) if layer.state.visible]

    @observe('selected')
    def _on_selected_change(self, change):
        selected = change["new"]
        with delay_callback(self.viewer.state, 'layers'):
            for index in range(len(self.layers)):
                self.viewer.layers[index].state.visible = index in selected

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
