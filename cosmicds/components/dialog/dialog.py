from ipyvuetify import VuetifyTemplate
from traitlets import Unicode, Bool

from ...utils import load_template


class Dialog(VuetifyTemplate):
    template = load_template("dialog.vue", __file__).tag(sync=True)
    dialog = Bool().tag(sync=True)
    launch_button_text = Unicode().tag(sync=True)
    title_text = Unicode().tag(sync=True)
    content_text = Unicode().tag(sync=True)
    accept_button_text = Unicode().tag(sync=True)

    def __init__(self, app, launch_button_text, title_text, content_text,
                 accept_button_text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._app = app
        self.launch_button_text = launch_button_text
        self.title_text = title_text
        self.content_text = content_text
        self.accept_button_text = accept_button_text

    def vue_accept_button_clicked(self, event):
        self.dialog = False
