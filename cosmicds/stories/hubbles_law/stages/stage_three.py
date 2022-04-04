from glue.core import Data
from glue.core.state_objects import State
from traitlets import default

from cosmicds.components.table import Table
from cosmicds.registries import register_stage
from cosmicds.phases import Stage
from cosmicds.utils import load_template
from cosmicds.viewers import CDSHistogramView, CDSScatterView

class StageState(State):
    pass

@register_stage(story="hubbles_law", index=3, steps=[
    "My data",
    "Class data",
    "Galaxy Type",
    "Professional Science Data"
])
class StageThree(Stage):
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

        measurements = self.get_data("student_measurements")
        fit_table = Table(self.session,
                          data=measurements,
                          glue_components=['ID',
                                          'Type',
                                          'velocity',
                                          'distance'],
                          key_component='ID',
                          names=['Galaxy Name',
                              'Galaxy Type',
                              'Velocity (km/s)',
                              'Distance (Mpc)'],
                          title='My Galaxies')
        self.add_widget(fit_table, label="fit_table")

        # Set up for student/class/all data
        measurements = self.get_data("student_measurements")
        student_dc_name = "student_data"
        student_cols = [x.label for x in measurements.main_components]
        dummy_data = {x : ['X'] if x in ['ID', 'Element', 'Type'] else [0] for x in student_cols}
        student_data = Data(label=student_dc_name, **dummy_data)
        self.add_data(student_data)
    
        class_dc_name = "HubbleData_ClassSample"
        all_dc_name = "HubbleData_All"
        class_data = self.get_data(class_dc_name)
        for component in class_data.components:
            field = component.label
            self.add_link(class_dc_name, field, all_dc_name, field)
            if component.label in student_data.component_ids():
                self.add_link(student_dc_name, field, class_dc_name, field)
        

        students_viewer = self.add_viewer(CDSScatterView, "students_viewer")
        fit_viewer = self.add_viewer(CDSScatterView, "fit_viewer")
        comparison_viewer = self.add_viewer(CDSScatterView, "comparison_viewer")
        morphology_viewer = self.add_viewer(CDSScatterView, "morphology_viewer")
        viewers = [
            students_viewer,
            fit_viewer,
            comparison_viewer,
            morphology_viewer
        ]
        for viewer in viewers:
            viewer.add_data(student_data)
            viewer.layers[-1].state.visible = False
            viewer.state.x_att = student_data.id['distance']
            viewer.state.y_att = student_data.id['velocity']

        