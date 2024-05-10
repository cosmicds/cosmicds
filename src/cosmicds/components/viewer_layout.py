import solara

__all__ = ["ToolBar", "ViewerLayout"]


@solara.component
def ToolBar(viewer):
    solara.Row(
        children=[
            viewer.toolbar,
            solara.v.Spacer(),
        ],
        margin=2,
        style={"align-items": "center"},
    )


@solara.component
def ViewerLayout(viewer):
    viewer.figure_widget.layout.height = 600
    layout = solara.Column(
        children=[
            ToolBar(viewer),
            viewer.figure_widget,
        ],
        margin=0,
        style={
            "height": "100%",
            "box-shadow": "0 3px 1px -2px rgba(0,0,0,.2),0 2px 2px 0 rgba(0,0,0,.14),0 1px 5px 0 rgba(0,0,0,.12) !important;",
        },
        classes=["elevation-2"],
    )
    with solara.Card(
        title=viewer.state.title,
        children=[layout]
    ):
        pass
