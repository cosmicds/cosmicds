from glue.config import viewer_tool
from glue.viewers.common.tool import Tool

@viewer_tool
class HomeTool(Tool):

    tool_id = 'cds:home'
    icon = 'glue_home'
    action_text = 'Home'
    tool_tip = 'Reset original zoom'
    mdi_icon = 'mdi-cached'

    def activate(self):
        self.viewer.reset_limits()
