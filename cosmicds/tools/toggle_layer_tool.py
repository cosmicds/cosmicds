from echo import CallbackProperty
from glue.config import viewer_tool
from glue.viewers.common.tool import Tool


@viewer_tool
class LayerToggleTool(Tool):
    toggled_count = CallbackProperty(0)

    tool_id = "cds:togglelayer"
    action_text = "Toggle display of a given layer"
    tool_tip = "Toggle display of data"
    mdi_icon = "mdi-toggle-switch-outline"

    def __init__(self, viewer, **kwargs):
        super().__init__(viewer, **kwargs)
        self.layer_to_toggle = None

    def activate(self):
        if self.layer_to_toggle is None:
            return

        # if we have no layers, don't do anything
        if len(self.viewer.layers) > 0:
            self.layer_to_toggle.state.visible = not self.layer_to_toggle.state.visible
            self.toggled_count += 1
    
    def set_layer_to_toggle(self, layer):
        self.layer_to_toggle = layer
