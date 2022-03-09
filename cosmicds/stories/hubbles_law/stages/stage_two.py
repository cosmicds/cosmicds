import logging

from echo import CallbackProperty
from glue.core.state_objects import State
from traitlets import default
from cosmicds.components.distance_sidebar.distance_sidebar import DistanceSidebar

from cosmicds.components.distance_tool import DistanceTool
from cosmicds.components.table import Table
from cosmicds.phases import Stage
from cosmicds.registries import register_stage
from cosmicds.stories.hubbles_law.utils import GALAXY_FOV, format_fov, format_measured_angle
from cosmicds.utils import load_template

log = logging.getLogger()

class StageState(State):
    selected_galaxy = CallbackProperty({})

@register_stage(story="hubbles_law", index=1, steps=[
    "Explore celestial sky",
    "Collect galaxy data",
    "Measure spectra",
    "Reflect",
    "Calculate velocities"
])
class StageTwo(Stage):
    @default('stage_state')
    def _default_state(self):
        return StageState()

    @default('template')
    def _default_template(self):
        return load_template("stage_two.vue", __file__)

    @default('title')
    def _default_title(self):
        return "Another Stage Name"

    @default('subtitle')
    def _default_subtitle(self):
        return "Perhaps a small blurb about this stage"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_component(DistanceTool(), label="c-distance-tool")

        distance_table = Table(self.session,
                               data=self.get_data('student_measurements'),
                               glue_components=['ID',
                                               'velocity',
                                               'distance'],
                               key_component='ID',
                               names=['Galaxy Name',
                                       'Velocity (km/s)',
                                       'Distance (Mpc)'],
                               title='My Galaxies | Distance Measurements',
                               single_select=True)
        self.add_widget(distance_table, label="distance_table")
        distance_table.observe(self.distance_table_selected_change, names=["selected"])

        self.add_component(DistanceSidebar(self.stage_state), label="c-distance-sidebar")
        self.distance_tool.observe(self._angular_size_update, names=["angular_size"])
        self.distance_tool.observe(self._angular_height_update, names=["angular_height"])

    def distance_table_selected_change(self, change):
        selected = change["new"]
        if not selected or selected == change["old"]:
            return

        index = self.distance_table.index
        data = self.distance_table.glue_data
        galaxy = { x.label : data[x][index] for x in data.main_components }
        self.distance_tool.go_to_location(galaxy["RA"], galaxy["DEC"], fov=GALAXY_FOV)

        self.stage_state.selected_galaxy = galaxy
        self.distance_tool.measuring_allowed = bool(galaxy)

    def _angular_size_update(self, change):
        self.distance_sidebar.angular_size = format_fov(change["new"])

    def _angular_height_update(self, change):
        self.distance_sidebar.angular_height = format_measured_angle(change["new"])

    @property
    def distance_sidebar(self):
        return self.get_component("c-distance-sidebar")

    @property
    def distance_tool(self):
        return self.get_component("c-distance-tool")
        
    @property
    def distance_table(self):
        return self.get_widget("distance_table")
