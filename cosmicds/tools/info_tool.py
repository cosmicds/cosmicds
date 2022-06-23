from glue.config import viewer_tool
from glue.viewers.common.tool import Tool

from traitlets import Bool, HasTraits

@viewer_tool
class InfoTool(Tool, HasTraits):

    tool_id = "cds:info"
    action_text = "Show information"
    tool_tip = "Show informational dialog"
    mdi_icon = "mdi-information-outline"

    active = Bool().tag(sync=True)

    def __init__(self, viewer, **kwargs):
        super().__init__(viewer, **kwargs)
    
    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False


