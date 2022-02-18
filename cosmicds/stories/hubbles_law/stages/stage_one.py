from glue.core.state_objects import State
from glue_jupyter.state_traitlets_helpers import GlueState
from glue_jupyter.bqplot.scatter import BqplotScatterView
from ipywidgets import widget_serialization
from pywwt.jupyter import WWTJupyterWidget
from traitlets import Dict, Unicode, default

from cosmicds.mixins import TemplateMixin
from cosmicds.registries import register_stage
from cosmicds.utils import load_template
from cosmicds.viewers.spectrum_view import SpectrumView
from cosmicds.events import StepChangeMessage
from cosmicds.phases import Stage
from cosmicds.components.table import Table

import logging
log = logging.getLogger()


class StageState(State):
    pass


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
        self.add_viewer(SpectrumView, label="spectrum_viewer")

        for label in ['hub_const_viewer', 'hub_fit_viewer',
                      'hub_comparison_viewer', 'hub_students_viewer',
                      'hub_morphology_viewer', 'hub_prodata_viewer']:
            self.add_viewer(BqplotScatterView, label=label)

        # Setup widgets
        galaxy_table = Table(self.session,
                             data=self.get_data("student_measurements"),
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
                             single_select=False)
        self.add_widget(galaxy_table, label="galaxy_table")

        wwt_viewer = WWTJupyterWidget()
        self.add_widget(wwt_viewer, label='wwt_viewer')
