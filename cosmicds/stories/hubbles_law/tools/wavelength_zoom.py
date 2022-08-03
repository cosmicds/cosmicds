from cosmicds.tools import BqplotXZoom
from glue.config import viewer_tool
from cosmicds.stories.hubbles_law.viewers import SpectrumViewerState


@viewer_tool #this decorator tells glue this is a viewer tool so it knows what to do with all this info
class WavelengthZoom(BqplotXZoom):

    icon = 'glue_zoom_to_rect'
    mdi_icon = "mdi-select-search"
    tool_id = 'hubble:wavezoom'
    action_text = 'x axis zoom'
    tool_tip = 'Zoom in on a region of the x-axis'

    on_zoom = None

    def update_selection(self, *args):
        old_state = SpectrumViewerState()
        old_state.update_from_state(self.viewer.state)
        if self.interact.brushing:
            return
        super().update_selection(*args)

        if self.on_zoom is not None:
            self.on_zoom(old_state, self.viewer.state)

        self.deactivate()