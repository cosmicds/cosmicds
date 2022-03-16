from glue.core.state_objects import State
from traitlets import default
from cosmicds.stories.hubbles_law.components import intro_slideshow

from cosmicds.stories.hubbles_law.components.intro_slideshow import IntroSlideshow
from cosmicds.phases import Stage
from cosmicds.registries import register_stage
from cosmicds.utils import load_template

class StageState(State):
    pass

@register_stage(story="hubbles_law", index=0, steps=[
    "Introduction"
])
class StageIntro(Stage):

    @default('template')
    def _default_template(self):
        return load_template("stage_intro.vue", __file__)

    @default('title')
    def _default_title(self):
        return "Introduction"

    @default('subtitle')
    def _default_subtitle(self):
        return "An introduction to Hubble's Law"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stage_state = StageState()
        intro_slideshow = IntroSlideshow()
        self.add_component(intro_slideshow, label='c-intro-slideshow')
        intro_slideshow.observe(self._on_slideshow_complete, names=['intro_complete'])

    def _on_slideshow_complete(self, change):
        if change["new"]:
            self.story_state.stage_index += 1
