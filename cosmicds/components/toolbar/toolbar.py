import os

from cosmicds.utils import load_template
from ipyvuetify import VuetifyTemplate
from traitlets import HasTraits, Dict, Instance, Unicode, Any, observe
from glue.viewers.common.tool import Tool, CheckableTool

class Toolbar(VuetifyTemplate):

    TOOL_ICONS = {
        'bqplot:xzoom' : 'mdi-select-search',
        'bqplot:yzoom': 'mdi-select-search',
        'bqplot:rectzoom': 'mdi-select-search',
        'bqplot:home' : 'mdi-cached',
        'bqplot:xrange': 'mdi-select-drag',
        'bqplot:yrange': 'mdi-select-drag',
        'bqplot:rectangle': 'mdi-select-drag',
    }

    template = load_template("toolbar.vue", __file__, traitlet=True).tag(sync=True)
    active_tool = Instance(Tool, allow_none=True,
                                     default_value=None)
    tools_data = Dict(default_value={}).tag(sync=True)
    active_tool_id = Any().tag(sync=True)

    def __init__(self, viewer, *args, **kwargs):
        self.tools = {}
        if viewer._default_mouse_mode_cls is not None:
            self._default_mouse_mode = viewer._default_mouse_mode_cls(viewer)
            self._default_mouse_mode.activate()
        else:
            self._default_mouse_mode = None
        super().__init__()

    @observe('active_tool_id')
    def _on_change_v_model(self, change):
        if change.new is not None:
            if isinstance(self.tools[change.new], CheckableTool):
                self.active_tool = self.tools[change.new]
            else:
                # In this case it is a non-checkable tool and we should
                # activate it but not keep the tool checked in the toolbar
                self.tools[change.new].activate()
                self.active_tool_id = None
        else:
            self.active_tool = None

    @observe('active_tool')
    def _on_change_active_tool(self, change):
        if change.old:
            change.old.deactivate()
        else:
            if self._default_mouse_mode:
                self._default_mouse_mode.deactivate()
        if change.new:
            change.new.activate()
            self.active_tool_id = change.new.tool_id
        else:
            self.active_tool_id = None
            if self._default_mouse_mode is not None:
                self._default_mouse_mode.activate()

    @classmethod
    def get_icon(cls, tool):
        if hasattr(tool, 'mdi_icon'):
            icon = tool.mdi_icon
        else:
            icon = cls.TOOL_ICONS.get(tool.tool_id, "")
        return icon

    def update_tools_data(self, tool):
        if tool.tool_id in self.tools_data:
            del self.tools_data[tool.tool_id]
        self.tools_data = {
            **self.tools_data, 
            tool.tool_id: {
                "tooltip" : tool.tool_tip,
                "icon": Toolbar.get_icon(tool)
            }
        }

    def refresh_tools_data(self, change):
        self.update_tools_data(change["owner"])

    def add_tool(self, tool):
        self.tools[tool.tool_id] = tool
        self.update_tools_data(tool)

        if isinstance(tool, HasTraits) and "tool_tip" in tool.traits():
            tool.observe(self.refresh_tools_data, names=["tool_tip"])

