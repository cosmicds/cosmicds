from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from traitlets import Bool, Dict, Instance, List, Unicode
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
    classes = List().tag(sync=True)

    def __init__(self, viewer, classes=None, style=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
