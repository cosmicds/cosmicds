from glue.config import viewer_tool


class RegisterTool():

    def __call__(self, tool_cls):
        try:
            viewer_tool(tool_cls)
        except ValueError:
            print(f"Tool ID {tool_cls.tool_id} already registered")
        return tool_cls


register_tool = RegisterTool()
