from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from traitlets import Bool, Dict, Instance, Int, List, Unicode, observe
from ipywidgets import DOMWidget

from ...utils import load_template


class ViewerLayout(VuetifyTemplate):
    template = load_template(
        "viewer_layout.vue", __file__, traitlet=True).tag(sync=True)
    controls = Dict().tag(sync=True, **widget_serialization)
    figure = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)
    css_style = Dict().tag(sync=True)
    show_toolbar = Bool(True).tag(sync=True)
    title = Unicode().tag(sync=True)
    show_subtitle = Bool(False).tag(sync=True)
    subtitle = Unicode().tag(sync=True)
    classes = List().tag(sync=True)
    viewer_width = Int().tag(sync=True)
    viewer_height = Int().tag(sync=True)

    def __init__(self, app, viewer_cls, classes=None, style=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        viewer = app.new_data_viewer(viewer_cls, show=False)
        self.viewer = viewer
        self.title = viewer.LABEL
        self.classes = classes or []
        self.show_toolbar = kwargs.get("show_toolbar", True)
        self.controls = dict(
            toolbar_selection_tools=viewer.toolbar_selection_tools,
            toolbar_selection_mode=viewer.toolbar_selection_mode,
            toolbar_active_subset=viewer.toolbar_active_subset)

        self.css_style = style or {'height': '300px'}
        self.figure = viewer.figure_widget


    @observe("viewer_width")
    def _on_width_update(self, change):
        self.viewer.state.viewer_width = change["new"]

    @observe("viewer_height")
    def _on_height_change(self, change):
        self.viewer.state.viewer_height = change["new"]

    def set_subtitle(self, text):
        if text:
            self.subtitle = text
            self.show_subtitle = True
        else:
            self.show_subtitle = False
            self.subtitle = " "
    
