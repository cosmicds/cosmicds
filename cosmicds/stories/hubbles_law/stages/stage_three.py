from echo import add_callback
from glue.core.message import NumericalDataChangedMessage
from glue.core.state_objects import State
from traitlets import default

from cosmicds.registries import register_stage
from cosmicds.stories.hubbles_law.stage import HubbleStage
from cosmicds.utils import load_template

from cosmicds.stories.hubbles_law.viewers import HubbleFitView

class StageState(State):
    pass

@register_stage(story="hubbles_law", index=3, steps=[
    "My data",
    "Class data",
    "Galaxy Type",
    "Professional Science Data"
])
class StageThree(HubbleStage):
    @default('stage_state')
    def _default_state(self):
        return StageState()

    @default('template')
    def _default_template(self):
        return load_template("stage_three.vue", __file__)
    
    @default('title')
    def _default_title(self):
        return "Explore Data"

    @default('subtitle')
    def _default_subtitle(self):
        return "Perhaps a small blurb about this stage"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fit_viewer = self.add_viewer(HubbleFitView, "fit_viewer", "My Data")
        student_data = self.get_data("student_data")
        fit_viewer.ignore(lambda x: x.label != student_data.label)
        fit_viewer.add_data(student_data)
        fit_viewer.state.x_att = student_data.id['distance']
        fit_viewer.state.y_att = student_data.id['velocity']

        add_callback(self.story_state, "reset_flag", self._on_reset)

        # Whenever the student data is updated, the student scatter viewer should update its bounds
        self.hub.subscribe(self, NumericalDataChangedMessage,
                           handler=self._on_student_data_change, filter=self._student_data_filter)

    def _student_data_filter(self, msg):
        return msg.data == self.get_data("student_data")

    def _on_student_data_change(self, msg):
        viewer = self.get_viewer("fit_viewer")
        viewer.state.reset_limits()

    def _on_reset(self, flag):
        print(flag)
        if flag:
            fit_viewer = self.get_viewer("fit_viewer")
            fit_tool = fit_viewer.toolbar.tools["cds:linefit"]
            fit_tool.deactivate()
