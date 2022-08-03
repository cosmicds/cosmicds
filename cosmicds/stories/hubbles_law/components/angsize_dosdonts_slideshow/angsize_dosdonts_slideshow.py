import ipyvuetify as v
from pathlib import Path
from traitlets import Int, Bool, Unicode, List
from cosmicds.utils import load_template
from glue_jupyter.state_traitlets_helpers import GlueState


# theme_colors()

class DosDonts_SlideShow(v.VuetifyTemplate):
    template = load_template(
        "angsize_dosdonts_slideshow.vue", __file__, traitlet=True).tag(sync=True)
    step = Int(0).tag(sync=True)
    length = Int(11).tag(sync=True)
    dialog = Bool(False).tag(sync=True)
    currentTitle = Unicode("").tag(sync=True)
    state = GlueState().tag(sync=True)
    max_step_completed = Int(0).tag(sync=True)

    _titles = [
        "Intro",
        "Blurry",
        "Elongated",
        "Hazy Elliptical Galaxies",
        "Faint Irregular Galaxies",
        "Measure the Entire Galaxy",
        "Field with Multiple Objects",
        "Zoomed In Galaxies",
        "Colliding Galaxies",
        "Galaxy Cluster",
        "That's It"
    ]
    _default_title = "Angular Size Dos and Don'ts"

    def __init__(self, story_state, *args, **kwargs):
        self.state = story_state
        self.currentTitle = self._default_title

        def update_title(change):
            index = change["new"]
            if index in range(len(self._titles)):
                self.currentTitle = self._titles[index]
            else:
                self.currentTitle = self._default_title

        self.observe(update_title, names=["step"])

        super().__init__(*args, **kwargs)
