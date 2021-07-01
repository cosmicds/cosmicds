from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization

from ...utils import load_template


class Footer(VuetifyTemplate):
    template = load_template("footer.vue", __file__).tag(sync=True)

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._app = app