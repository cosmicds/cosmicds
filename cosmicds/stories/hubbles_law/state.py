from pathlib import Path

from echo import CallbackProperty, DictCallbackProperty, ignore_callback

from cosmicds.phases import Story
from cosmicds.registries import story_registry
import numpy as np
from glue.core import Data
import ipyvuetify as v

import requests
from cosmicds.utils import API_URL
from cosmicds.stories.hubbles_law.utils import HUBBLE_ROUTE_PATH, H_ALPHA_REST_LAMBDA

def reverse(d):
    return { v : k for k, v in d.items() }

MEAS_TO_STATE = {
    "measwave": "obs_wave_value",
    "restwave": "rest_wave_value",
    "velocity": "velocity_value",
    "distance": "est_dist_value",
    "name": "galaxy_name",
    "student_id": "student_id",
    "angular_size" : "ang_size_value"
}

STATE_TO_MEAS = reverse(MEAS_TO_STATE)

@story_registry(name="hubbles_law")
class HubblesLaw(Story):
    measurements = DictCallbackProperty({})
    calculations = DictCallbackProperty({})
    validation_failure_counts = DictCallbackProperty({})
    responses = DictCallbackProperty({})
    reset_flag = CallbackProperty(False)
    sample_measurement = DictCallbackProperty({})

    measurement_keys = [
        "obs_wave_value",
        "rest_wave_value",
        "velocity_value",
        "est_dist_value",
        "ang_size_value",
        "ra",
        "decl",
        "name",
        "z",
        "type",
        "element",
        "student_id",
        "last_modified",
        "measurement_number"
    ]
    summary_keys = [
        "hubble_fit_value",
        "age_value"
    ]
    name_ext = ".fits"

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
        galaxy = requests.get(f"{API_URL}/{HUBBLE_ROUTE_PATH}/sample-galaxy").json()
        self.data_collection.append(Data(
            label="Sample_Galaxy",
            **{ k : [galaxy[k]] for k in galaxy }
        ))

        # Compose empty data containers to be populated by user
        student_cols = ["id", "name", "ra", "decl", "z", "type", "measwave",
                         "restwave", "student_id", "velocity", "distance",
                         "element", "angular_size", "measurement_number"]
        student_measurements = Data(
            label='student_measurements',
            **{x: np.array([], dtype='float64')
               for x in student_cols})
        student_data = Data(
            label="student_data",
            **{x : ['X'] if x in ['id', 'element', 'type', 'name', 'measurement_number'] else [0] 
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

        self.galaxy_index = 0

    def make_data_writeable(self, data):
        for comp in data.main_components:
            data[comp.label].setflags(write=True)

    def prune_none(self, data):
        keep = set()
        for i in range(data.size):
            if all(data[comp][i] is not None for comp in data.main_components):
                keep.add(i)

        pruned_components = { comp.label: [data[comp][x] for x in keep] for comp in data.main_components }
        pruned = Data(label=data.label, **pruned_components)
        data.update_values_from_data(pruned)

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
        if new_data.size > 0:
            student_data = dc['student_data']
            student_data.update_values_from_data(new_data)
            self.make_data_writeable(student_data)

    def reset_data(self):
        dc = self.data_collection
        student_cols = ["id", "name", "ra", "decl", "z", "type", "measwave",
                         "restwave", "student_id", "velocity", "distance",
                         "element", "angular_size", "measurement_number"]
        student_measurements = Data(
            label='student_measurements',
            **{x: np.array([], dtype='float64')
               for x in student_cols})
        student_data = Data(
            label="student_data",
            **{x : ['X'] if x in ['id', 'element', 'type', 'name', 'measurement_number'] else [0] 
                for x in student_cols})
        dc["student_measurements"].update_values_from_data(student_measurements)
        dc["student_data"].update_values_from_data(student_data)

    def start_over(self):
        self.reset_data()
        self.stage_index = 1
        self.reset_flag = True
        with ignore_callback(self, 'reset_flag'):
            self.reset_flag = False

    def data_from_measurements(self, measurements):
        for measurement in measurements:
            measurement.update(measurement.get("galaxy", {}))

        galaxy = self.sample_galaxy()
        for i in range(len(measurements), 2):
            measurement = dict(galaxy)
            number = "first" if i == 0 else "second"
            measurement["rest_wave_value"] = H_ALPHA_REST_LAMBDA
            measurement["measurement_number"] = number
            measurements.append(measurement)
        
        components = { STATE_TO_MEAS.get(k, k) : [m.get(k, None) for m in measurements] for k in self.measurement_keys }
        for i, name in enumerate(components["name"]):
            if name.endswith(self.name_ext):
                components["name"][i] = name[:-len(self.name_ext)]
        return Data(**components)

    def fetch_measurements(self, url):
        response = requests.get(url)
        res_json = response.json()
        return res_json["measurements"]

    def fetch_measurement_data_and_update(self, url, label, prune_none=False, make_writeable=False, check_update=None, callbacks=None):
        measurements = self.fetch_measurements(url)
        need_update = check_update is None or check_update(measurements)
        if not need_update or len(measurements) == 0:
            return None
        new_data = self.data_from_measurements(measurements)
        new_data.label = label
        if prune_none:
            self.prune_none(new_data)
        data = self.data_collection[label]
        data.update_values_from_data(new_data)
        if make_writeable:
            self.make_data_writeable(data)

        if callbacks is not None:
            for cb in callbacks:
                cb()

        return new_data

    def fetch_sample_data(self):
        sample_meas_url = f"{API_URL}/{HUBBLE_ROUTE_PATH}/sample-measurements/{self.student_user['id']}"
        self.fetch_measurement_data_and_update(sample_meas_url, "student_measurements", make_writeable=True)
        self.update_student_data()

    def sample_galaxy(self):
        sample_data = self.data_collection["Sample_Galaxy"]
        galaxy = { k.label : sample_data[k][0] for k in sample_data.main_components }
        return galaxy
