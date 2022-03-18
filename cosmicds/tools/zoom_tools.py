from bqplot.interacts import BrushIntervalSelector, BrushSelector
from echo import delay_callback
from glue.config import viewer_tool
from glue_jupyter.bqplot.common.tools import InteractCheckableTool, INTERACT_COLOR

class BqplotZoom(InteractCheckableTool):
    
    def __init__(self, viewer, **kwargs):
        super().__init__(viewer, **kwargs)
        self._reset_interact()
    
    def _reset_interact(self):
        raise NotImplementedError("Subclass must implement _reset_interact")
        
    def _selected(self):
        raise NotImplementedError("Subclass must implement _selected")
        
    def update_selection(self, *args):
        if self.interact.brushing:
            return
        
        x, y = self._selected()
        if x is None or y is None:
            return
        
        state = self.viewer.state
        with delay_callback(state, 'x_min', 'x_max', 'y_min', 'y_max'):
            state.x_min, state.x_max = min(x), max(x)
            state.y_min, state.y_max = min(y), max(y)

        self._reset_interact()
        self.activate()
        
    def deactivate(self):
        super().deactivate()
        self.viewer.toolbar.active_tool = None


@viewer_tool
class BqplotRectangleZoom(BqplotZoom):

    icon = 'glue_zoom_to_rect'
    tool_id = 'bqplot:rectzoom'
    action_text = '2D zoom'
    tool_tip = 'Zoom in on a rectangular region'

    def __init__(self, viewer, **kwargs):
        super().__init__(viewer, **kwargs)
        self._reset_interact()
    
    def _reset_interact(self):
        if hasattr(self, 'interact'):
            self.interact.close()
        self.interact = BrushSelector(x_scale=self.viewer.scale_x,
                                      y_scale=self.viewer.scale_y,
                                      color=INTERACT_COLOR)
        self.interact.observe(self.update_selection, "brushing")
        
    def _selected(self):
        return self.interact.selected_x, self.interact.selected_y


@viewer_tool
class BqplotXZoom(BqplotZoom):
    icon = 'glue_zoom_to_rect'
    tool_id = 'bqplot:xzoom'
    action_text = 'x axis zoom'
    tool_tip = 'Zoom in on a region of the x-axis'
        
    def _reset_interact(self):
        if hasattr(self, 'interact'):
            self.interact.close()
        self.interact = BrushIntervalSelector(scale=self.viewer.scale_x,
                                              color=INTERACT_COLOR)
        self.interact.observe(self.update_selection, "brushing")
        
    def _selected(self):
        return self.interact.selected, [self.viewer.state.y_min, self.viewer.state.y_max]


@viewer_tool
class BqplotYZoom(BqplotZoom):
    icon = 'glue_zoom_to_rect'
    tool_id = 'bqplot:yzoom'
    action_text = 'y axis zoom'
    tool_tip = 'Zoom in on a region of the y-axis'
        
    def _reset_interact(self):
        if hasattr(self, 'interact'):
            self.interact.close()
        self.interact = BrushIntervalSelector(scale=self.viewer.scale_y,
                                              orientation='vertical',
                                              color=INTERACT_COLOR)
        self.interact.observe(self.update_selection, "brushing")
        
    def _selected(self):
        return [self.viewer.state.x_min, self.viewer.state.x_max], self.interact.selected
