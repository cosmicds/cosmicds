from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from traitlets import Dict, Instance
from ipywidgets import DOMWidget

from ...utils import load_template


class WidgetLayout(VuetifyTemplate):
    template = load_template("widget_layout.vue", __file__).tag(sync=True)
    css_style = Dict().tag(sync=True)
    widget = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)

    def __init__(self, widget, style=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = widget
        self.css_style = style or {'height': '300px'}
