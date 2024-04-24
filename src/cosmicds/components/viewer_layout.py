from glue.viewers.common.viewer import Viewer
from reacton import ipyvuetify as rv
import solara

@solara.component
def ViewerLayout(
    viewer: Viewer,
):
    layout = solara.Column(
        children=[viewer.figure_widget.element()]
    )
    
