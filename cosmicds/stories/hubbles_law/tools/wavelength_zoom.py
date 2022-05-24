from cosmicds.tools import BqplotXZoom
from glue.config import viewer_tool


@viewer_tool #this decorator tells glue this is a viewer tool so it knows what to do with all this info
class WavelengthZoom(BqplotXZoom):

    icon = 'glue_zoom_to_rect'
    mdi_icon = "mdi-select-drag"
    tool_id = 'hubble:wavezoom'
    action_text = 'x axis zoom'
    tool_tip = 'Zoom in on a region of the x-axis'

    def update_selection(self, *args):
        if self.interact.brushing:
            return
        super().update_selection(*args)

        self.deactivate()