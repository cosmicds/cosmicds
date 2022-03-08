from unicodedata import name
from echo import CallbackProperty
from glue.core.state_objects import State
from glue_jupyter.state_traitlets_helpers import GlueState
from glue_jupyter.bqplot.scatter import BqplotScatterView
from ipywidgets import widget_serialization
from pywwt.jupyter import WWTJupyterWidget
from random import sample
from traitlets import Dict, Unicode, default

from cosmicds.mixins import TemplateMixin
from cosmicds.registries import register_stage
from cosmicds.utils import load_template
from cosmicds.viewers.spectrum_view import SpectrumView
from cosmicds.events import StepChangeMessage
from cosmicds.phases import Stage
from cosmicds.components.table import Table
from cosmicds.components.selection_tool import SelectionTool
from cosmicds.stories.hubbles_law.utils import GALAXY_FOV, H_ALPHA_REST_LAMBDA, MG_REST_LAMBDA

import logging
log = logging.getLogger()


class StageState(State):
    gals_total = CallbackProperty(0)
    gals_max = CallbackProperty(5)

@register_stage(story="hubbles_law", index=0, steps=[
    "Explore celestial sky",
    "Collect galaxy data",
    "Measure spectra",
    "Reflect",
    "Calculate velocities"
])
class StageOne(Stage):
    @default('stage_state')
    def _default_state(self):
        return StageState()

    @default('template')
    def _default_template(self):
        return load_template("stage_one.vue", __file__)

    @default('title')
    def _default_title(self):
        return "Collect Galaxy Data"

    @default('subtitle')
    def _default_subtitle(self):
        return "Perhaps a small blurb about this stage"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup viewers
        spectrum_viewer = self.add_viewer(SpectrumView, label="spectrum_viewer")
        spectrum_viewer.add_event_callback(self.on_spectrum_click, events=['click'])

        for label in ['hub_const_viewer', 'hub_fit_viewer',
                      'hub_comparison_viewer', 'hub_students_viewer',
                      'hub_morphology_viewer', 'hub_prodata_viewer']:
            self.add_viewer(BqplotScatterView, label=label)

        # Setup widgets
        galaxy_table = Table(self.session,
                             data=self.get_data('student_measurements'),
                             glue_components=['ID',
                                              'Element',
                                              'restwave',
                                              'measwave',
                                              'velocity'],
                             key_component='ID',
                             names=['Galaxy Name',
                                    'Element',
                                    'Rest Wavelength (Å)',
                                    'Observed Wavelength (Å)',
                                    'Velocity (km/s)',
                                    'Distance (Mpc)',
                                    'Galaxy Type'],
                             title='My Galaxies | Velocity Measurements',
                             single_select=True) # True for now
        self.add_widget(galaxy_table, label="galaxy_table")
        galaxy_table.row_click_callback = self.on_galaxy_row_click
        galaxy_table.observe(self.galaxy_table_selected_change, names=["selected"])

        # Setup components
        sdss_data = self.get_data("SDSS_all_sample_filtered")
        selection_tool = SelectionTool(data=sdss_data)
        self.add_component(selection_tool, label='c-selection-tool')
        selection_tool.on_galaxy_selected = self._on_galaxy_selected

    def _on_galaxy_selected(self, galaxy):
        data = self.get_data("student_measurements")
        already_present = galaxy['ID'] in data['ID'] # Avoid duplicates
        if already_present:
            # To do nothing
            return
            # If instead we wanted to remove the point from the student's selection
            # index = next(idx for idx, val in enumerate(component_dict['ID']) if val == galaxy['ID'])
            # for component, values in component_dict.items():
            #     values.pop(index)
        else:
            self.add_data_values("student_measurements", galaxy)

    def vue_select_galaxies(self, _args=None):
        data = self.get_data("dummy_student_data")
        components = [x.label for x in data.main_components]
        measurements = self.get_data("student_measurements")
        need = self.selection_tool.gals_max - measurements.size
        indices = sample(range(data.size), need)
        for index in indices:
            galaxy = { c: data[c][index] for c in components }
            self.selection_tool.select_galaxy(galaxy)

    def update_spectrum_viewer(self, name, z):
        filename = name
        specview = self.get_viewer("spectrum_viewer")
        spec_name = filename.split(".")[0]
        data_name = spec_name + '[COADD]'
        spec_data = self.get_data(data_name)
        self.story_state.update_data("spectrum_data", spec_data)
        specview.state.reset_limits()

        sdss = self.get_data("SDSS_all_sample_filtered")
        sdss_index = next((i for i in range(sdss.size) if sdss["ID"][i] == name), None)
        if sdss_index is not None:
            element = sdss['Element'][sdss_index]
            specview.update(element, z)
            restwave = MG_REST_LAMBDA if element == 'Mg-I' else H_ALPHA_REST_LAMBDA
            index = self.get_widget("galaxy_table").index
            self.update_data_value("student_measurements", "Element", element, index)
            self.update_data_value("student_measurements", "restwave", restwave, index)


    def galaxy_table_selected_change(self, change):
        if change["new"] == change["old"]:
            return

        index = self.galaxy_table.index
        data = self.galaxy_table.glue_data
        galaxy = { x.label : data[x][index] for x in data.main_components }
        name = galaxy["ID"]
        gal_type = galaxy["Type"]
        if name is None or gal_type is None:
            return

        # Load the spectrum data, if necessary
        filename = name
        spec_data = self.story_state.load_spectrum_data(filename, gal_type)

        # If this is the first selection we're making
        # we want to move the app forward
        # TODO

        # Update the data in the spectrum viewer,
        # if we're far enough in the story
        # TODO: Express this condition in the right way
        z = galaxy["Z"]
        self.story_state.update_data("spectrum_data", spec_data)
        specview = self.get_viewer("spectrum_viewer")
        if len(specview.layers) == 0:
            specview.add_data(spec_data)
        self.update_spectrum_viewer(name, z)

    def on_galaxy_row_click(self, item, _data=None):
        index = self.galaxy_table.indices_from_items([item])[0]
        data = self.galaxy_table.glue_data
        name = data["ID"][index]
        gal_type = data["Type"][index]
        if name is None or gal_type is None:
            return
        self.selection_tool.go_to_galaxy(data["RA"][index], data["DEC"][index], fov=GALAXY_FOV)

    def on_spectrum_click(self, event):
        if event["event"] != "click":
            return
        value = round(event["domain"]["x"], 2)
        self.update_data_value("student_measurements", "measwave", value, self.galaxy_table.index)

    @property
    def selection_tool(self):
        return self.get_component("c-selection-tool")

    @property
    def galaxy_table(self):
        return self.get_widget("galaxy_table")
