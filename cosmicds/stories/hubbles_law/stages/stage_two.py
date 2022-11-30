from functools import partial
import logging

from astropy.modeling import fitting, models
import astropy.units as u
from echo import CallbackProperty, add_callback, ignore_callback
from glue.core.state_objects import State
from numpy import pi
from traitlets import default, Bool, Float
from cosmicds.events import WriteToDatabaseMessage

from cosmicds.stories.hubbles_law.components.distance_sidebar import DistanceSidebar
from cosmicds.stories.hubbles_law.components.distance_tool import DistanceTool
from cosmicds.components.table import Table
from cosmicds.registries import register_stage
from cosmicds.stories.hubbles_law.utils import FULL_FOV, GALAXY_FOV, MILKY_WAY_SIZE_MPC, age_in_gyr_simple, format_fov, format_measured_angle
from cosmicds.utils import load_template
from cosmicds.stories.hubbles_law.stage import HubbleStage

log = logging.getLogger()

class StageState(State):
    galaxy = CallbackProperty({})
    galaxy_dist = CallbackProperty(None)
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
    age_to_display = Float(0).tag(sync=True)
    display_age = Bool(False).tag(sync=True)

    @default('template')
    def _default_template(self):
        return load_template("stage_two.vue", __file__)

    @default('title')
    def _default_title(self):
        return "Distance Measurements"

    @default('subtitle')
    def _default_subtitle(self):
        return ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stage_state = StageState()

        self.add_component(DistanceTool(), label="c-distance-tool-1")
        self.add_component(DistanceTool(), label="c-distance-tool-2")

        distance_table = Table(self.session,
                               data=self.get_data('student_measurements'),
                               glue_components=['name',
                                               'distance',
                                               'angular_size',
                                               'measurement_number'],
                               key_component='name',
                               names=['Galaxy Name',
                                       'Distance (Mpc)',
                                       'Angular Size',
                                       'Number'],
                               title='My Galaxies | Distance Measurements',
                               single_select=True)
        self.add_widget(distance_table, label="distance_table")
        distance_table.observe(self.distance_table_selected_change, names=["selected"])

        self.add_component(DistanceSidebar(self.stage_state), label="c-distance-sidebar-1")
        self.distance_tool_1.observe(partial(self._angular_size_update, num=1), names=["angular_size"])
        self.distance_tool_1.observe(partial(self._angular_height_update, num=1), names=["angular_height"])
        self.distance_sidebar_1.angular_height = format_fov(self.distance_tool_1.angular_height)

        self.add_component(DistanceSidebar(self.stage_state), label="c-distance-sidebar-2")
        self.distance_tool_2.observe(partial(self._angular_size_update, num=2), names=["angular_size"])
        self.distance_tool_2.observe(partial(self._angular_height_update, num=2), names=["angular_height"])
        self.distance_sidebar_2.angular_height = format_fov(self.distance_tool_2.angular_height)

        add_callback(self.story_state, 'stage_index', self._on_stage_index_change)

    def _on_stage_index_change(self, index):
        if index == 2:
            galaxy = self.story_state.sample_galaxy()
            self.distance_table.selected = [galaxy]

    def distance_table_selected_change(self, change):
        selected = change["new"]
        if not selected or selected == change["old"]:
            return

        data = self.distance_table.glue_data
        galaxy = { x.label : data[x][0] for x in data.main_components }
        self.distance_tool_1.reset_canvas()
        self.distance_tool_2.reset_canvas()
        self.distance_tool_1.go_to_location(galaxy["ra"], galaxy["decl"], fov=GALAXY_FOV)
        self.distance_tool_2.go_to_location(galaxy["ra"], galaxy["decl"], fov=GALAXY_FOV)

        self.stage_state.galaxy = galaxy
        self.stage_state.galaxy_dist = None
        self.distance_tool_1.measuring_allowed = bool(galaxy)
        self.distance_tool_2.measuring_allowed = bool(galaxy)
        self.distance_tool_1.galaxy = galaxy
        self.distance_tool_2.galaxy = galaxy

    def _angular_size_update(self, change, num):
        new_ang_size = change["new"]
        self.get_component(f"c-distance-sidebar-{num}").angular_size = format_fov(new_ang_size)
        if new_ang_size != 0 and new_ang_size is not None:
            self._make_measurement(num)

    def _angular_height_update(self, change, num):
        self.get_component(f"c-distance-sidebar-{num}").angular_height = format_measured_angle(change["new"])

    def _make_measurement(self, num):
        index = num - 1
        angular_size = self.get_component(f"c-distance-tool-{num}").angular_size
        ang_size_deg = angular_size.value
        distance = round(MILKY_WAY_SIZE_MPC * 180 / (ang_size_deg * pi))
        angular_size_as = round(angular_size.to(u.arcsec).value)
        self.stage_state.galaxy_dist = distance
        self.update_data_values("student_measurements", {
            "distance": distance,
            "angular_size": angular_size_as
        }, index)
        self.story_state.update_student_data()

    def _find_H0(self):
        data = self.get_data("student_data")
        x = data["distance"]
        y = data["velocity"]
        fit = fitting.LinearLSQFitter()
        line_init = models.Linear1D(intercept=0, fixed={'intercept':True})
        fitted_line = fit(line_init, x, y)
        return fitted_line.slope.value

    def vue_submit(self, _args=None):
        h0 = self._find_H0()
        age = age_in_gyr_simple(h0)
        self.story_state.calculations["age_value"] = age
        self.age_to_display = age
        self.display_age = True
        self.hub.broadcast(WriteToDatabaseMessage(self))

    def vue_start_over(self, _args=None):
        self.app_state.reset_student = True
        self.distance_tool_1.reset_canvas()
        self.distance_tool_2.reset_canvas()
        self.distance_tool_1.go_to_location(0, 0, FULL_FOV)
        self.distance_tool_2.go_to_location(0, 0, FULL_FOV)
        self.display_age = False
        self.story_state.start_over()
        self.distance_table.selected = []
        self.distance_table.selected = self.distance_table.items

    @property
    def distance_sidebar_1(self):
        return self.get_component("c-distance-sidebar-1")

    @property
    def distance_sidebar_2(self):
        return self.get_component("c-distance-sidebar-2")

    @property
    def distance_tool_1(self):
        return self.get_component("c-distance-tool-1")

    @property
    def distance_tool_2(self):
        return self.get_component("c-distance-tool-2")
        
    @property
    def distance_table(self):
        return self.get_widget("distance_table")
