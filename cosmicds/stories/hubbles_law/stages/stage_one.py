from os.path import join
from pathlib import Path

from echo import add_callback, ignore_callback, CallbackProperty
from glue.core import Data
from glue.core.state_objects import State
from glue_jupyter.bqplot.scatter import BqplotScatterView
import ipyvuetify as v
from numpy import isin
from random import sample
from traitlets import default, Bool

import astropy.units as u
from astropy.coordinates import Angle, SkyCoord

from cosmicds.registries import register_stage
from cosmicds.utils import load_template, update_figure_css
from cosmicds.stories.hubbles_law.viewers import SpectrumView, spectrum_view
from cosmicds.stories.hubbles_law.stage import HubbleStage
from cosmicds.components.table import Table
from cosmicds.stories.hubbles_law.data.styles import load_style
from cosmicds.stories.hubbles_law.components import DopplerCalc, SpectrumSlideshow, SelectionTool
from cosmicds.components.generic_state_component import GenericStateComponent
from cosmicds.stories.hubbles_law.utils import GALAXY_FOV, H_ALPHA_REST_LAMBDA, MG_REST_LAMBDA

import logging
log = logging.getLogger()


class StageState(State):
    gals_total = CallbackProperty(0)
    gals_max = CallbackProperty(5)
    gal_selected = CallbackProperty(False)
    spec_viewer_reached = CallbackProperty(False)
    spec_tutorial_opened = CallbackProperty(False)
    lambda_used = CallbackProperty(False)
    lambda_on = CallbackProperty(False)
    waveline_set = CallbackProperty(False)
    obswaves_total = CallbackProperty(0)
    velocity_button = CallbackProperty(False)
    velocities_total = CallbackProperty(0)

    marker = CallbackProperty("")
    indices = CallbackProperty({})
    image_location = CallbackProperty()
    lambda_rest = CallbackProperty(0)
    lambda_obs = CallbackProperty(0)
    element = CallbackProperty("")
    reflection_complete = CallbackProperty(False)
    doppler_calc_dialog = CallbackProperty(True) # Should the doppler calculation be displayed when marker == dop_cal5?
    student_vel = CallbackProperty(0) # Value of student's calculated velocity
    doppler_calc_complete = CallbackProperty(False) # Did student finish the doppler calculation?

    markers = CallbackProperty([
        'mee_gui1',
        'sel_gal1',
        'sel_gal2',
        'sel_gal3',
        'cho_row1',
        'mee_spe1',
        'res_wav1',
        'obs_wav1',
        'obs_wav2',        
        'rep_rem1',
        'ref_dat1',
        'dop_cal0',
        'dop_cal1',
        'dop_cal2',
        'dop_cal3',
        'dop_cal4',
        'dop_cal5',
        'dop_cal6'
    ])

    step_markers = CallbackProperty([
        'mee_gui1',
        'mee_spe1',
        'ref_dat1',
        'dop_cal0',
    ])

    csv_highlights = CallbackProperty([
        'sel_gal1',
        'sel_gal2',
        'sel_gal3',
    ])

    table_highlights = CallbackProperty([
        'cho_row1',
        'dop_cal3',
        'dop_cal4',
        'dop_cal5',
        'dop_cal6',
    ])

    spec_highlights = CallbackProperty([
        'mee_spe1',
        'res_wav1',
        'obs_wav1',
        'obs_wav2',        
        'rep_rem1',
        'ref_dat1',
        'dop_cal0',
        'dop_cal1',
        'dop_cal2',
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.marker = self.markers[0]
        self.indices = {marker: idx for idx, marker in enumerate(self.markers)}

    def marker_before(self, marker):
        return self.indices[self.marker] < self.indices[marker]


@register_stage(story="hubbles_law", index=1, steps=[
    #"Explore celestial sky",
    "Collect galaxy data",
    "Measure spectra",
    "Reflect",
    "Calculate velocities"
])

class StageOne(HubbleStage):
    show_team_interface = Bool(False).tag(sync=True)
    START_COORDINATES = SkyCoord(180 * u.deg, 25 * u.deg, frame='icrs')

    @default('template')
    def _default_template(self):
        return load_template("stage_one.vue", __file__)

    @default('title')
    def _default_title(self):
        return "Spectra and Velocities"

    @default('subtitle')
    def _default_subtitle(self):
        return "Perhaps a small blurb about this stage"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stage_state = StageState()
        self.show_team_interface = self.app_state.show_team_interface
        
        self.stage_state.image_location = join("data", "images", "stage_one_spectrum")
        add_callback(self.app_state, 'using_voila', self._update_image_location)

        # Set up viewers
        spectrum_viewer = self.add_viewer(
            SpectrumView, label="spectrum_viewer")
        spectrum_viewer.add_event_callback(
            self.on_spectrum_click, events=['click'])
        sf_tool = spectrum_viewer.toolbar.tools["hubble:specflag"]
        add_callback(sf_tool, "flagged", self._on_spectrum_flagged)

        for label in ['hub_const_viewer', 'hub_fit_viewer',
                      'hub_comparison_viewer', 'hub_students_viewer',
                      'hub_morphology_viewer', 'hub_prodata_viewer']:
            self.add_viewer(BqplotScatterView, label=label)

        add_velocities_tool = \
            dict(id="update-velocities",
                 icon="mdi-run-fast",
                 tooltip="Fill in velocities",
                 disabled=True,
                 activate=self.update_velocities)
        galaxy_table = Table(self.session,
                             data=self.get_data('student_measurements'),
                             glue_components=['name',
                                              'element',
                                              'restwave',
                                              'measwave',
                                              'velocity'],
                             key_component='name',
                             names=['Galaxy Name',
                                    'Element',
                                    'Rest Wavelength (Å)',
                                    'Observed Wavelength (Å)',
                                    'Velocity (km/s)'],

                             title='My Galaxies',
                             selected_color=self.table_selected_color(self.app_state.dark_mode),
                             use_subset_group=False,
                             single_select=True, # True for now
                             tools=[add_velocities_tool])

        self.add_widget(galaxy_table, label="galaxy_table")
        galaxy_table.row_click_callback = self.on_galaxy_row_click
        galaxy_table.observe(
            self.galaxy_table_selected_change, names=["selected"])

        # Set up components
        sdss_data = self.get_data("SDSS_all_sample_filtered")
        selection_tool = SelectionTool(data=sdss_data, state=self.stage_state)
        self.add_component(selection_tool, label='c-selection-tool')
        selection_tool.on_galaxy_selected = self._on_galaxy_selected
        selection_tool.observe(self._on_selection_tool_flagged, names=['flagged'])

        spectrum_slideshow = SpectrumSlideshow(self.stage_state)
        self.add_component(spectrum_slideshow, label='c-spectrum-slideshow')

        #spectrum_slideshow.observe(self._on_slideshow_complete, names=['spectrum_slideshow_complete'])

        # Set up the generic state components
        state_components_dir = str(
            Path(__file__).parent.parent / "components" / "generic_state_components" / "stage_one")
        path = join(state_components_dir, "")
        state_components = [
            "guideline_intro_guidelines",
            "guideline_select_galaxies_1",
            "guideline_select_galaxies_2",
            "guideline_select_galaxies_3",
            "guideline_notice_galaxy_table",
            "guideline_choose_row",
            "guideline_spectrum",
            "guideline_restwave",
            "guideline_obswave_1",
            "guideline_obswave_2",
            "guideline_remaining_gals",
            "guideline_reflect_on_data",
            "guideline_doppler_calc_0",
            "guideline_doppler_calc_1",
            "guideline_doppler_calc_2",
            "guideline_doppler_calc_3"
        ]
        ext = ".vue"
        for comp in state_components:
            label = f"c-{comp}".replace("_", "-")

            # comp + ext = filename; path = folder where they live.
            component = GenericStateComponent(comp + ext, path, self.stage_state)
            self.add_component(component, label=label)

        # Set up doppler calc components
        doppler_calc_components_dir = str(Path(__file__).parent.parent / "components" / "doppler_calc_components")
        path = join(doppler_calc_components_dir,"")
        doppler_components = [
            "guideline_doppler_calc_4",
            "slideshow_doppler_calc_5",
            "guideline_doppler_calc_6"
        ]
        for comp in doppler_components:
            label = f"c-{comp}".replace("_", "-")
            component = DopplerCalc(comp + ext, path, self.stage_state, self.story_state)
            self.add_component(component, label=label)

        # execute add_student_velocity when student_vel_calc in c-doppler-calc-5-slideshow is updated.
        doppler_slideshow = self.get_component("c-slideshow-doppler-calc-5")
        doppler_slideshow.observe(self.add_student_velocity, names=["student_vel_calc"])

        # Callbacks
        def update_count(change):
            self.stage_state.gals_total = change["new"]
        selection_tool.observe(update_count, names=['selected_count'])
        add_callback(self.stage_state, 'marker',
                     self._on_marker_update, echo_old=True)
        add_callback(self.story_state, 'step_index',
                     self._on_step_index_update)
        self.trigger_marker_update_cb = True

        self.update_spectrum_style(dark=self.app_state.dark_mode)


        add_callback(self.stage_state, 'doppler_calc_complete', self.enable_velocity_tool)

        spectrum_viewer = self.get_viewer("spectrum_viewer")
        restwave_tool = spectrum_viewer.toolbar.tools["hubble:restwave"]
        add_callback(restwave_tool, 'lambda_used', self._on_lambda_used)
        add_callback(restwave_tool, 'lambda_on', self._on_lambda_on)
        for tool_id in ["hubble:restwave", "hubble:wavezoom", "bqplot:home"]:
            spectrum_viewer.toolbar.set_tool_enabled(tool_id, False)

    def _on_marker_update(self, old, new):
        if not self.trigger_marker_update_cb:
            return
        markers = self.stage_state.markers
        advancing = markers.index(new) > markers.index(old)
        if new in self.stage_state.step_markers and advancing:
            self.story_state.step_complete = True
            self.story_state.step_index = self.stage_state.step_markers.index(new)
        if advancing and old == "sel_gal3":
            self.galaxy_table.selected = []
            self.selection_tool.widget.center_on_coordinates(self.START_COORDINATES, instant=True)
        if advancing and new == "cho_row1" and self.galaxy_table.index is not None:
            self.stage_state.spec_viewer_reached = True
            self.stage_state.marker = "mee_spe1"
        if advancing and old == "dop_cal2":
            self.galaxy_table.selected = []
            self.selection_tool.widget.center_on_coordinates(self.START_COORDINATES, instant=True)
        if advancing and new == "res_wav1":
            spectrum_viewer = self.get_viewer("spectrum_viewer")
            spectrum_viewer.toolbar.set_tool_enabled("hubble:restwave", True)
        if advancing and new == "obs_wav2":
            spectrum_viewer = self.get_viewer("spectrum_viewer")
            spectrum_viewer.toolbar.set_tool_enabled("hubble:wavezoom", True)
            spectrum_viewer.toolbar.set_tool_enabled("bqplot:home", True)

    def _on_step_index_update(self, index):
        # Change the marker without firing the associated stage callback
        # We can't just use ignore_callback, since other stuff (i.e. the frontend)
        # may depend on marker callbacks
        self.trigger_marker_update_cb = False
        self.stage_state.marker = self.stage_state.step_markers[index]
        self.trigger_marker_update_cb = True

    def _on_galaxy_selected(self, galaxy):
        data = self.get_data("student_measurements")
        is_in = isin(data['name'], galaxy['name']) # Avoid duplicates
        already_present = is_in.size > 0 and is_in[0]
        if already_present:
            # To do nothing
            return
            # If instead we wanted to remove the point from the student's selection
            # index = next(idx for idx, val in enumerate(component_dict['ID']) if val == galaxy['ID'])
            # for component, values in component_dict.items():
            #     values.pop(index)
        else:
            filename = galaxy['name']
            gal_type = galaxy['type']
            galaxy.pop("element")
            self.story_state.load_spectrum_data(filename, gal_type)
            self.add_data_values("student_measurements", galaxy)
            self.galaxy_table.selected = [{'name': filename}]

    def _on_lambda_used(self, used):
        self.stage_state.lambda_used = used

    def _on_lambda_on(self, on):
        self.stage_state.lambda_on = on

    def _select_from_data(self, dc_name):
        data = self.get_data(dc_name)
        components = [x.label for x in data.main_components]
        measurements = self.get_data("student_measurements")
        need = self.selection_tool.gals_max - measurements.size
        indices = sample(range(data.size), need)
        for index in indices:
            galaxy = {c: data[c][index] for c in components}
            self.selection_tool.select_galaxy(galaxy)

    def vue_fill_data(self, _args=None):
        self._select_from_data("dummy_student_data")
        self.galaxy_table.selected = []
        self.selection_tool.widget.center_on_coordinates(self.START_COORDINATES, instant=True)
        self.stage_state.marker = "sel_gal3"  

    def vue_select_galaxies(self, _args=None):
        self._select_from_data("SDSS_all_sample_filtered")
        self.galaxy_table.selected = []
        self.selection_tool.widget.center_on_coordinates(self.START_COORDINATES, instant=True)
        self.stage_state.marker = "sel_gal3"        

    def update_spectrum_viewer(self, name, z):
        specview = self.get_viewer("spectrum_viewer")
        specview.toolbar.active_tool = None
        filename = name
        spec_name = filename.split(".")[0]
        data_name = spec_name + '[COADD]'
        data = self.get_data(data_name)
        self.story_state.update_data("spectrum_data", data)
        if len(specview.layers) == 0:
            spec_data = self.get_data("spectrum_data")
            specview.add_data(spec_data)
            specview.figure.axes[0].label = "Wavelength (Angstroms)"
            specview.figure.axes[1].label = "Brightness"
        specview.state.reset_limits()
        self.stage_state.waveline_set = False

        sdss = self.get_data("SDSS_all_sample_filtered")
        sdss_index = next((i for i in range(sdss.size) if sdss["name"][i] == name), None)
        if sdss_index is not None:
            element = sdss['element'][sdss_index]
            specview.update(name, element, z)
            restwave = MG_REST_LAMBDA if element == 'Mg-I' else H_ALPHA_REST_LAMBDA
            index = self.get_widget("galaxy_table").index
            self.update_data_value("student_measurements", "element", element, index)
            self.update_data_value("student_measurements", "restwave", restwave, index)
            self.stage_state.element = element

    def galaxy_table_selected_change(self, change):
        if change["new"] == change["old"]:
            return

        index = self.galaxy_table.index
        if index is None:
            self._empty_spectrum_viewer()
            return
        data = self.galaxy_table.glue_data
        galaxy = { x.label : data[x][index] for x in data.main_components }
        name = galaxy["name"]
        gal_type = galaxy["type"]
        if name is None or gal_type is None:
            return

        self.selection_tool.current_galaxy = galaxy

        # Load the spectrum data, if necessary
        filename = name
        spec_data = self.story_state.load_spectrum_data(filename, gal_type)

        z = galaxy["z"]
        self.story_state.update_data("spectrum_data", spec_data)
        self.update_spectrum_viewer(name, z)

        if self.stage_state.marker == 'cho_row1':
            self.stage_state.spec_viewer_reached = True
            self.stage_state.marker = 'mee_spe1'

    def on_galaxy_row_click(self, item, _data=None):
        index = self.galaxy_table.indices_from_items([item])[0]
        data = self.galaxy_table.glue_data
        name = data["name"][index]
        gal_type = data["type"][index]
        if name is None or gal_type is None:
            return

        self.selection_tool.go_to_location(data["ra"][index], data["decl"][index], fov=GALAXY_FOV)
        self.stage_state.lambda_rest = data["restwave"][index]
        self.stage_state.lambda_obs = data["measwave"][index]
        self.stage_state.sel_gal_index = index

    def on_spectrum_click(self, event):
        specview = self.get_viewer("spectrum_viewer")
        if event["event"] != "click" or not specview.line_visible:
            return

        new_value = round(event["domain"]["x"], 0)
        index = self.galaxy_table.index
        data = self.galaxy_table.glue_data
        curr_value = data["measwave"][index]

        if curr_value is None:
            self.stage_state.obswaves_total = self.stage_state.obswaves_total + 1

        self.stage_state.waveline_set = True
        self.stage_state.lambda_obs = new_value

        if index is not None:
            self.update_data_value("student_measurements", "measwave", new_value, index)
            self.story_state.update_student_data()

    def vue_add_current_velocity(self, _args=None):
        data = self.get_data("student_measurements")
        index = self.galaxy_table.index
        if index is not None:
            lamb_obs = data["restwave"][index]
            lamb_meas = data["measwave"][index]
            velocity = round((3 * (10 ** 5) * (lamb_meas/lamb_obs - 1)),0)
            self.update_data_value("student_measurements", "velocity", velocity, index)
            self.story_state.update_student_data()

    def add_student_velocity(self, _args=None):
        index = self.galaxy_table.index
        velocity = round(self.stage_state.student_vel)
        self.update_data_value("student_measurements", "velocity", velocity, index)
        self.stage_state.velocities_total = self.stage_state.velocities_total + 1

    @property
    def selection_tool(self):
        return self.get_component("c-selection-tool")

    @property
    def slideshow(self):
        return self.get_component('c-spectrum-slideshow')

    def _update_image_location(self, using_voila):
        prepend = "voila/files/" if using_voila else ""
        self.stage_state.image_location = prepend + "data/images/stage_one_spectrum"

    @property
    def galaxy_table(self):
        return self.get_widget("galaxy_table")

    def update_spectrum_style(self, dark):
        spectrum_viewer = self.get_viewer("spectrum_viewer")
        theme_name = "dark" if dark else "light"
        style = load_style(f"default_spectrum_{theme_name}")
        update_figure_css(spectrum_viewer, style_dict=style)

    def _on_dark_mode_change(self, dark):
        super()._on_dark_mode_change(dark)
        self.update_spectrum_style(dark)

    def _empty_spectrum_viewer(self):
        dc_name = "spectrum_data"
        spec_data = self.get_data(dc_name)
        data = Data(label=spec_data.label, **{
            c.label: [0] for c in spec_data.main_components
        })
        spectrum_viewer = self.get_viewer("spectrum_viewer")
        self.story_state.update_data(dc_name, data)
        spectrum_viewer.update("", "", 0)

    def _on_selection_tool_flagged(self, change):
        if not change["new"]:
            return
        index = self.galaxy_table.index
        if index is None:
            return
        item = self.galaxy_table.selected[0]
        galaxy_name = item["name"]
        self.remove_measurement(galaxy_name)
        self.selection_tool.flagged = False

    def _on_spectrum_flagged(self, flagged):
        if not flagged:
            return
        #index = self.galaxy_table.index
        item = self.galaxy_table.selected[0]
        galaxy_name = item["name"]
        self.remove_measurement(galaxy_name)
        self._empty_spectrum_viewer()

        spectrum_viewer = self.get_viewer("spectrum_viewer")
        sf_tool = spectrum_viewer.toolbar.tools["hubble:specflag"]
        with ignore_callback(sf_tool, "flagged"):
            sf_tool.flagged = False

    def update_velocities(self, table, tool):
        data = table.glue_data
        for item in table.items:
            index = table.indices_from_items([item])[0]
            if index is not None and data["velocity"][index] is None:
                lamb_obs = data["restwave"][index]
                lamb_meas = data["measwave"][index]
                if lamb_obs is None or lamb_meas is None:
                    continue
                velocity = round((3 * (10 ** 5) * (lamb_meas/lamb_obs - 1)),0)
                self.update_data_value("student_measurements", "velocity", velocity, index)
                self.stage_state.velocities_total = self.stage_state.velocities_total + 1
        self.story_state.update_student_data()
        table.update_tool(tool)

    def enable_velocity_tool(self, enable):
        if enable:
            tool = self.galaxy_table.get_tool("update-velocities")
            tool["disabled"] = False
            self.galaxy_table.update_tool(tool)
