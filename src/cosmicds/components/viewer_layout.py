from cosmicds.utils import make_figure_autoresize
import solara
import reacton.ipyvuetify as rv

__all__ = ["ToolBar", "ViewerLayout"]


@solara.component
def ToolBar(viewer):
    if viewer.state.title is not None:
        title = viewer.state.title
    else:
        title = ""

    solara.Row(
        children=[
            solara.Text(title, style={"padding-left": "1ch", "text-transform": "uppercase", "height": "48px", "align-content": "center", "font-size": "1.3rem"}),
            solara.v.Spacer(),
            viewer.toolbar,
        ],
        margin=0,
        style= {"background-color": "var(--primary)", "border-bottom-left-radius": "0px", "border-bottom-right-radius": "0px", "color": "white"},
    )

@solara.component
def ViewerLayout(viewer):
    make_figure_autoresize(viewer.figure_widget, 400)
    # viewer.figure_widget.layout.height = 600
    layout = solara.Column(
        children=[
            ToolBar(viewer),
            viewer.figure_widget,
        ],
        gap="0px",
        margin=0,
        style={
            "height": "100%",
            "width": "100%",
            "box-shadow": "0 3px 1px -2px rgba(0,0,0,.2),0 2px 2px 0 rgba(0,0,0,.14),0 1px 5px 0 rgba(0,0,0,.12) !important;",
        },
        classes=["elevation-2 mb-4"],
    )
    with rv.Card(
        children=[layout]
    ):
        pass
