from echo import add_callback, CallbackProperty
from glue.core.state_objects import State
from traitlets import default

from cosmicds.stories.hubbles_law.components.two_intro_slideshow import TwoIntroSlideShow
from cosmicds.phases import Stage
from cosmicds.registries import register_stage
from cosmicds.utils import load_template

class StageState(State):
    image_location = CallbackProperty()

@register_stage(story="hubbles_law", index=2, steps=[
    "Angular Distances"
])
class StageTwoIntro(Stage):

    @default('template')
    def _default_template(self):
        return load_template("stage_two_intro.vue", __file__)

    @default('title')
    def _default_title(self):
        return "Stage 2 Introduction"

    @default('subtitle')
    def _default_subtitle(self):
        return "An introduction to Angular Distances"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stage_state = StageState()
        two_intro_slideshow = TwoIntroSlideShow(self.stage_state, self.app_state)
        self.add_component(two_intro_slideshow, label='c-two-intro-slideshow')
        two_intro_slideshow.observe(self._on_slideshow_complete, names=['two_intro_complete'])
        self.stage_state.image_location = "data/images"

    @property
    def slideshow(self):
        return self.get_component('c-two-intro-slideshow')

    def _on_slideshow_complete(self, change):
        if change["new"]:
            self.story_state.stage_index = 3

            # We need to do this so that the stage will be moved forward every
            # time the button is clicked, not just the first
            self.slideshow.two_intro_complete = False
