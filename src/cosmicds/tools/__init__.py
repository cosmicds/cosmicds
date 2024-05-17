from glue.config import viewer_tool

from .line_fit_tool import LineFitTool  # noqa


class RegisterTool():

    def __call__(self, tool_cls):
        try:
            viewer_tool(tool_cls)
        except ValueError:
            print(f"Tool ID {tool_cls.tool_id} already registered")


register_tool = RegisterTool()
