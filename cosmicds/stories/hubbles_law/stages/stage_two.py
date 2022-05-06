import logging

from echo import CallbackProperty, add_callback
from glue.core.state_objects import State
from traitlets import default

from cosmicds.stories.hubbles_law.components.distance_sidebar import DistanceSidebar
from cosmicds.stories.hubbles_law.components.distance_tool import DistanceTool
from cosmicds.components.table import Table
from cosmicds.registries import register_stage
from cosmicds.stories.hubbles_law.utils import GALAXY_FOV, format_fov, format_measured_angle
from cosmicds.utils import load_template
from cosmicds.stories.hubbles_law.stage import HubbleStage

log = logging.getLogger()

class StageState(State):
    selected_galaxy = CallbackProperty({})
    make_measurement = CallbackProperty(False)
    marker = CallbackProperty("")
    advance_marker = CallbackProperty(True)

    markers = CallbackProperty([
        "test"
    ])

    step_markers = CallbackProperty({

    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.marker_index = 0
        self.marker = self.markers[0]
        add_callback(self, 'advance_marker', self.move_marker_forward)

    def move_marker_forward(self, _value=None):
        self.marker_index = min(self.marker_index + 1, len(self.markers) - 1)
        self.marker = self.markers[self.marker_index]

    def index(self, marker):
        return self.markers.index(marker)

@register_stage(story="hubbles_law", index=2, steps=[
    "Measure distances"
])
class StageTwo(HubbleStage):

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

        self.stage_state = StageState()

        self.add_component(DistanceTool(), label="c-distance-tool")

        distance_table = Table(self.session,
                               data=self.get_data('student_measurements'),
                               glue_components=['name',
                                               'velocity',
                                               'distance'],
                               key_component='name',
                               names=['Galaxy Name',
                                       'Velocity (km/s)',
                                       'Distance (Mpc)'],
                               title='My Galaxies | Distance Measurements',
                               color=self.table_selected_color(self.app_state.dark_mode),
                               single_select=True)
        self.add_widget(distance_table, label="distance_table")
        distance_table.observe(self.distance_table_selected_change, names=["selected"])

        self.add_component(DistanceSidebar(self.stage_state), label="c-distance-sidebar")
        self.distance_tool.observe(self._angular_size_update, names=["angular_size"])
        self.distance_tool.observe(self._angular_height_update, names=["angular_height"])

        add_callback(self.stage_state, 'make_measurement', self._make_measurement)

    def distance_table_selected_change(self, change):
        selected = change["new"]
        if not selected or selected == change["old"]:
            return

        index = self.distance_table.index
        data = self.distance_table.glue_data
        galaxy = { x.label : data[x][index] for x in data.main_components }
        self.distance_tool.go_to_location(galaxy["ra"], galaxy["decl"], fov=GALAXY_FOV)

        self.stage_state.selected_galaxy = galaxy
        self.distance_tool.measuring_allowed = bool(galaxy)

    def _angular_size_update(self, change):
        self.distance_sidebar.angular_size = format_fov(change["new"])

    def _angular_height_update(self, change):
        self.distance_sidebar.angular_height = format_measured_angle(change["new"])

    def _make_measurement(self, value):
        if not value:
            return
        galaxy = self.stage_state.selected_galaxy
        index = self.get_data_index('student_data', 'id', lambda x: x == galaxy["id"])

        

    @property
    def distance_sidebar(self):
        return self.get_component("c-distance-sidebar")

    @property
    def distance_tool(self):
        return self.get_component("c-distance-tool")
        
    @property
    def distance_table(self):
        return self.get_widget("distance_table")
