import requests

from echo import CallbackProperty
from glue.config import viewer_tool
from glue.viewers.common.tool import Tool

from cosmicds.utils import API_URL

@viewer_tool
class SpectrumFlagTool(Tool):

    tool_id = "hubble:specflag"
    action_text = "Flag a spectrum as bad"
    tool_tip = "Flag a spectrum as bad"
    mdi_icon = "mdi-flag"

    flagged = CallbackProperty(False)

    def activate(self):
        galaxy_name = self.viewer.spectrum_name
        if not galaxy_name.endswith(".fits"):
            galaxy_name += ".fits"
        data = { "galaxy_name": galaxy_name }
        requests.post(f"{API_URL}/mark-spectrum-bad", json=data)
        self.flagged = True

