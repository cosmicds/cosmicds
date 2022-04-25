from pathlib import Path

from echo import DictCallbackProperty

from cosmicds.phases import Story
from cosmicds.registries import story_registry
import numpy as np
from glue.core import Data
import ipyvuetify as v

import requests
from cosmicds.utils import API_URL

@story_registry(name="hubbles_law")
class HubblesLaw(Story):
    measurements = DictCallbackProperty({
        "galax_id": 123,
        "rest_wave_value": 6563.0,
        "rest_wave_unit": "Angstrom",
        "obs_wave_value": 6863.0,
        "obs_wave_unit": "Angstrom",
        "velocity_value": 120.0,
        "velocity_unit": "km / s",
        "ang_size": 50,
        "est_dist_value": 100,
        "est_dist_unit": "lyr"
    })
    calculations = DictCallbackProperty({
        "hubble_value_fit_value": 65.0,
        "hubble_value_fit_unit": "km / s / Mpc",
        "hubble_value_guess_value": 80.0,
        "hubble_value_guess_unit": "km / s / Mpc",
        "age_value": 1.3e9,
        "age_unit": "Gyr"
    })
    validation_failure_counts = DictCallbackProperty({
        "doppler_equation": 1,
        "final_velocity": 3,
        "mc_q1": 2
    })
    responses = DictCallbackProperty({
        "dialog1": {
            "free_response": "I'm 90% confident about my answer.",
            "finished": True
        }
    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._set_theme()

        # Load data needed for Hubble's Law
        data_dir = Path(__file__).parent / "data"
        output_dir = data_dir / "hubble_simulation" / "output"

        # Load some simulated measurements as summary data
        self.app.load_data([
            f"{dataset}.csv" for dataset in (
                data_dir / "galaxy_data",
                data_dir / "Hubble 1929-Table 1",
                data_dir / "HSTkey2001",
                data_dir / "dummy_student_data",
                #data_dir / "SDSS_all_sample_filtered",
                output_dir / "HubbleData_ClassSample",
                output_dir / "HubbleData_All",
                output_dir / "HubbleSummary_ClassSample",
                output_dir / "HubbleSummary_Students",
                output_dir / "HubbleSummary_Classes",
            )
        ])

        # Load in the galaxy data
        galaxies = requests.get(f"{API_URL}/galaxies").json()
        self.data_collection.append(Data(
            label="SDSS_all_sample_filtered",
            **{ k : [x[k] for x in galaxies] for k in galaxies[0] }
        ))

        # Compose empty data containers to be populated by user
        student_cols = ["id", "name", "ra", "decl", "z", "type", "measwave",
                         "restwave", "student_id", "velocity", "distance",
                         "element", "angular_size"]
        student_measurements = Data(
            label='student_measurements',
            **{x: np.array([], dtype='float64')
               for x in student_cols})
        student_data = Data(
            label="student_data",
            **{x : ['X'] if x in ['id', 'element', 'type'] else [0] 
                for x in student_cols})
        self.data_collection.append(student_measurements)
        self.data_collection.append(student_data)

        self.app.add_link(student_measurements, 'id', student_data, 'id')
        self.app.add_link(student_measurements, 'distance', student_data, 'distance')
        self.app.add_link(student_measurements, 'velocity', student_data, 'velocity')
        self.app.add_link(student_measurements, 'student_id', student_data, 'student_id')

        # Make all data writeable
        for data in self.data_collection:
            self.make_data_writeable(data)

    def make_data_writeable(self, data):
        for comp in data.main_components:
            data[comp.label].setflags(write=True)

    def _set_theme(self):
        v.theme.dark = True
        v.theme.themes.dark.primary = 'colors.lightBlue.darken4'   # Overall theme & header bars
        v.theme.themes.light.primary = 'colors.lightBlue.darken4'
        v.theme.themes.dark.secondary = 'colors.pink.darken3'    # Headers on dialogs & buttons that pop up dialogs
        v.theme.themes.light.secondary = 'colors.pink.darken2'
        v.theme.themes.dark.accent = 'colors.amber.accent2'   # Next/Back buttons
        v.theme.themes.light.accent = 'colors.amber.accent3'
        v.theme.themes.dark.error = 'colors.teal.accent2'  # Team insider buttons that will not appear for user
        v.theme.themes.light.error = 'colors.teal.accent3'
        v.theme.themes.dark.info = 'colors.deepOrange.darken3'  # Instruction scaffolds & viewer highlights
        v.theme.themes.light.info = 'colors.deepOrange.lighten2'
        v.theme.themes.dark.success = 'colors.green'   # Unallocated
        v.theme.themes.light.success = 'colors.green'
        v.theme.themes.dark.warning = '' # Unallocated
        v.theme.themes.light.warning = ''
        v.theme.themes.dark.anchor = '' # Unallocated
        v.theme.themes.light.anchor = ''

    def load_spectrum_data(self, spectrum, gal_type):
        type_folders = {
            "Sp" : "spirals_spectra",
            "E" : "ellipticals_spectra",
            "Ir" : "irregulars_spectra"
        }
        name = spectrum.split(".")[0]
        spectra_path = Path(__file__).parent / "data" / "spectra"
        folder = spectra_path / type_folders[gal_type]
        path = str(folder / spectrum)
        data_name = name + '[COADD]'

        # Don't load data that we've already loaded
        dc = self.data_collection
        if data_name not in dc:
            self.app.load_data(path, label=name)
            data = dc[data_name]
            data['lambda'] = 10 ** data['loglam']
            dc.remove(dc[name + '[SPECOBJ]'])
            dc.remove(dc[name + '[SPZLINE]'])
            self.make_data_writeable(data)
        return dc[data_name]

    def update_data(self, label, new_data):
        dc = self.data_collection
        if label in dc:
            data = dc[label]
            data.update_values_from_data(new_data)
            data.label = label
        else:
            main_comps = [x.label for x in new_data.main_components]
            components = { col: list(new_data[col]) for col in main_comps }
            data = Data(label=label, **components)
            self.make_data_writeable(data) 
            dc.append(data)

    def update_student_data(self):
        dc = self.data_collection
        data = dc['student_measurements']
        df = data.to_dataframe()
        df = df[df['distance'].notna() & df['velocity'].notna()]
        main_components = [x.label for x in data.main_components]
        components = { col: list(df[col]) for col in main_components }
        new_data = Data(label='student_data', **components)
        student_data = dc['student_data']
        student_data.update_values_from_data(new_data)
        self.make_data_writeable(student_data)
