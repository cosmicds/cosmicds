from os.path import join
from pathlib import Path

from echo import CallbackProperty, add_callback, ignore_callback
from glue.core.state_objects import State
from numpy import pi
from traitlets import default, Bool

import astropy.units as u
from astropy.coordinates import Angle, SkyCoord

from cosmicds.registries import register_stage
from cosmicds.utils import load_template
from cosmicds.stories.hubbles_law.stage import HubbleStage
from cosmicds.components.table import Table
from cosmicds.stories.hubbles_law.components import Angsize_SlideShow, DistanceSidebar, DistanceTool
from cosmicds.components.generic_state_component import GenericStateComponent
from cosmicds.stories.hubbles_law.utils import GALAXY_FOV, MILKY_WAY_SIZE_MPC, format_fov, format_measured_angle

import logging
log = logging.getLogger()


class StageState(State):
    galaxy = CallbackProperty({})
    galaxy_selected = CallbackProperty(False)
    galaxy_dist = CallbackProperty(None)
    ruler_clicked = CallbackProperty(False)
    make_measurement = CallbackProperty(False)
    marker = CallbackProperty("")
    advance_marker = CallbackProperty(True)
    image_location = CallbackProperty()
    distance_sidebar = CallbackProperty(False)

    markers = CallbackProperty([
        'ang_siz1',
        'cho_row1',
        'ang_siz2',
        'ang_siz3',
        'ang_siz4',
        'ang_siz5',
        'ang_siz6',
        'rep_rem1',
        'est_dis1',
        'est_dis2',
        'cho_row2',
        'est_dis3',
        'est_dis4',
        'fil_rem1',
        'two_com1',
    ])

    step_markers = CallbackProperty([
        'ang_siz1',
    ])

    csv_highlights = CallbackProperty([
        'ang_siz1',
        'ang_siz2',
        'ang_siz3',
        'ang_siz4',
        'ang_siz5',
        'ang_siz6',
        'rep_rem1',
        'est_dis1',
        'est_dis2',
    ])

    table_highlights = CallbackProperty([
        'cho_row1',
        'cho_row2',
        'est_dis3',
        'est_dis4',
        'fil_rem1',
        'two_com1',
    ])

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
    "Measure angular size"
])
class StageTwo(HubbleStage):
    show_team_interface = Bool(False).tag(sync=True)
    START_COORDINATES = SkyCoord(180 * u.deg, 25 * u.deg, frame='icrs')

    @default('template')
    def _default_template(self):
        return load_template("stage_two.vue", __file__)

    @default('title')
    def _default_title(self):
        return "Galaxy Distances"

    @default('subtitle')
    def _default_subtitle(self):
        return "Perhaps a small blurb about this stage"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stage_state = StageState()
        self.show_team_interface = self.app_state.show_team_interface

        angsize_slideshow = Angsize_SlideShow(self.stage_state)
        self.add_component(angsize_slideshow, label='c-angsize-slideshow')

        self.add_component(DistanceTool(self.stage_state), label="c-distance-tool")
        self.stage_state.image_location = "data/images/stage_two_distance"

        type_names = { "E" : "Elliptical", "Ir": "Irregular", "Sp": "Spiral" }
        distance_table = Table(self.session,
                               data=self.get_data('student_measurements'),
                               glue_components=['name',
                                                'type',
                                                'angular_size',
                                                'distance'],
                               key_component='name',
                               transforms={ 'type' : lambda x: type_names.get(x, x) },
                               names=['Galaxy Name',
                                      'GZ Class',
                                      'θ (arcsec)',
                                      'Distance (Mpc)'],
                               title='My Galaxies',
                               selected_color=self.table_selected_color(self.app_state.dark_mode),
                               use_subset_group=False,
                               single_select=True)

        self.add_widget(distance_table, label="distance_table")
        distance_table.observe(
            self.distance_table_selected_change, names=["selected"])

        self.add_component(DistanceSidebar(self.stage_state), label="c-distance-sidebar")
        self.distance_tool.observe(self._angular_size_update, names=["angular_size"])
        self.distance_tool.observe(self._angular_height_update, names=["angular_height"])
        self.distance_sidebar.angular_height = format_fov(self.distance_tool.angular_height)

        self.distance_tool.observe(self._distance_tool_flagged, names=["flagged"])
        add_callback(self.stage_state, 'make_measurement',
                     self._make_measurement)



        # Set up the generic state components
        state_components_dir = str(
            Path(__file__).parent.parent / "components" / "generic_state_components" / "stage_two")
        path = join(state_components_dir, "")
        state_components = [
            "guideline_angsize_meas1",
            "guideline_choose_row1",
            "guideline_angsize_meas2",
            "guideline_angsize_meas3",
            "guideline_angsize_meas4",
            "guideline_angsize_meas5",
            "guideline_angsize_meas6",
            "guideline_repeat_remaining_galaxies",
            "guideline_estimate_distance1",
            "guideline_estimate_distance2",
            "guideline_choose_row2",
            "guideline_estimate_distance3",
            "guideline_estimate_distance4",
            "guideline_fill_remaining_galaxies",
            "guideline_stage_two_complete"
        ]
        ext = ".vue"
        for comp in state_components:
            label = f"c-{comp}".replace("_", "-")

            # comp + ext = filename; path = folder where they live.
            component = GenericStateComponent(comp + ext, path, self.stage_state)
            self.add_component(component, label=label)

        # Callbacks
        add_callback(self.stage_state, 'marker',
                     self._on_marker_update, echo_old=True)
        add_callback(self.story_state, 'step_index',
                     self._on_step_index_update)
        self.trigger_marker_update_cb = True


    def _on_marker_update(self, old, new):
        if not self.trigger_marker_update_cb:
            return
        markers = self.stage_state.markers
        advancing = markers.index(new) > markers.index(old)
        if advancing and new == "cho_row1":
            self.distance_table.selected = []
            self.distance_tool.widget.center_on_coordinates(self.START_COORDINATES, instant=True)

    def _on_step_index_update(self, index):
        # Change the marker without firing the associated stage callback
        # We can't just use ignore_callback, since other stuff (i.e. the frontend)
        # may depend on marker callbacks
        self.trigger_marker_update_cb = False
        self.stage_state.marker = self.stage_state.step_markers[index]
        self.trigger_marker_update_cb = True

    def distance_table_selected_change(self, change):
        selected = change["new"]
        if not selected or selected == change["old"]:
            return

        index = self.distance_table.index
        data = self.distance_table.glue_data
        galaxy = { x.label : data[x][index] for x in data.main_components }
        self.distance_tool.reset_canvas()
        self.distance_tool.go_to_location(galaxy["ra"], galaxy["decl"], fov=GALAXY_FOV)

        self.stage_state.galaxy = galaxy
        self.stage_state.galaxy_dist = None
        self.distance_tool.measuring_allowed = bool(galaxy)

        if self.stage_state.marker == 'cho_row1':
            self.stage_state.marker = 'ang_siz2'
            self.stage_state.galaxy_selected = True

    def _angular_size_update(self, change):
        self.distance_sidebar.angular_size = format_measured_angle(change["new"])

    def _angular_height_update(self, change):
        self.distance_sidebar.angular_height = format_fov(change["new"])

    def _make_measurement(self, value):
        if not value:
            return
        galaxy = self.stage_state.galaxy
        index = self.get_data_indices('student_measurements', 'name', lambda x: x == galaxy["name"], single=True)
        angular_size = self.distance_tool.angular_size
        ang_size_deg = angular_size.value
        distance = round(MILKY_WAY_SIZE_MPC * 180 / (ang_size_deg * pi))
        angular_size_as = round(angular_size.to(u.arcsec).value)
        self.stage_state.galaxy_dist = distance
        self.update_data_value("student_measurements", "distance", distance, index)
        self.update_data_value("student_measurements", "angular_size", angular_size_as, index)
        self.story_state.update_student_data()
        with ignore_callback(self.stage_state, 'make_measurement'):
            self.stage_state.make_measurement = False

    def _distance_tool_flagged(self, change):
        if not change["new"]:
            return
        index = self.distance_table.index
        if index is None:
            return
        item = self.distance_table.selected[0]
        galaxy_name = item["name"]
        self.remove_measurement(galaxy_name)
        self.distance_tool.flagged = False

    @property
    def distance_sidebar(self):
        return self.get_component("c-distance-sidebar")

    @property
    def distance_tool(self):
        return self.get_component("c-distance-tool")

    @property
    def distance_table(self):
        return self.get_widget("distance_table")
