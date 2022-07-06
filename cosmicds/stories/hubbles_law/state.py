from pathlib import Path

from echo import DictCallbackProperty

from cosmicds.phases import Story
from cosmicds.registries import story_registry
import numpy as np
from glue.core.component import CategoricalComponent, Component
from glue.core import Data
import ipyvuetify as v

import requests
from cosmicds.utils import API_URL, RepeatedTimer
from cosmicds.stories.hubbles_law.utils import HUBBLE_ROUTE_PATH
from cosmicds.stories.hubbles_law.data_management import STATE_TO_MEAS

@story_registry(name="hubbles_law")
class HubblesLaw(Story):
    measurements = DictCallbackProperty({})
    calculations = DictCallbackProperty({})
    validation_failure_counts = DictCallbackProperty({})
    responses = DictCallbackProperty({})

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
        "student_id"
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
        galaxies = requests.get(f"{API_URL}/{HUBBLE_ROUTE_PATH}/galaxies").json()
        galaxies_dict = { k : [x[k] for x in galaxies] for k in galaxies[0] }
        galaxies_dict["name"] = [x[:-len(self.name_ext)] for x in galaxies_dict["name"]]
        self.data_collection.append(Data(
            label="SDSS_all_sample_filtered",
            **galaxies_dict
        ))

        # Compose empty data containers to be populated by user
        self.student_cols = ["name", "ra", "decl", "z", "type", "measwave",
                         "restwave", "student_id", "velocity", "distance",
                         "element", "angular_size"]
        self.categorical_cols = ['name', 'element', 'type']
        student_measurements = Data(label="student_measurements")
        class_data = Data(label="class_data")
        student_data = Data(label="student_data")
        for col in self.student_cols:
            categorical = col in self.categorical_cols
            ctype = CategoricalComponent if categorical else Component
            meas_comp = ctype(np.array([]))
            data = ['X'] if categorical else [0]
            student_data_comp = ctype(np.array(data))
            class_data_comp = ctype(np.array(data))
            student_measurements.add_component(meas_comp, col)
            student_data.add_component(student_data_comp, col)
            class_data.add_component(class_data_comp, col)

        self.data_collection.append(student_measurements)
        self.data_collection.append(student_data)
        self.data_collection.append(class_data)
        for comp in ['distance', 'velocity', 'student_id']:
            self.app.add_link(student_measurements, comp, student_data, comp)
            self.app.add_link(student_measurements, comp, class_data, comp)

        # Make all data writeable
        for data in self.data_collection:
            HubblesLaw.make_data_writeable(data)

        self.class_data_timer = RepeatedTimer(30, self.fetch_class_data)
        self.class_data_timer.start()

    def _set_theme(self):
        v.theme.dark = True
        v.theme.themes.dark.primary = 'colors.lightBlue.darken4'   # Overall theme & header bars
        v.theme.themes.light.primary = 'colors.lightBlue.darken3'
        v.theme.themes.dark.secondary = 'colors.cyan.darken3'    # Headers on dialogs & buttons that pop up dialogs
        v.theme.themes.light.secondary = 'colors.cyan.darken2'
        v.theme.themes.dark.accent = 'colors.amber.accent2'   # Next/Back buttons
        v.theme.themes.light.accent = 'colors.amber.accent3'
        v.theme.themes.dark.error = 'colors.green.accent3'  # Team insider buttons that will not appear for user
        v.theme.themes.light.error = 'colors.green.accent3'
        v.theme.themes.dark.info = 'colors.deepOrange.darken3'  # Instruction scaffolds & viewer highlights
        v.theme.themes.light.info = 'colors.deepOrange.darken1'
        v.theme.themes.dark.success = 'colors.indigo.darken2'   # Unallocated
        v.theme.themes.light.success = 'colors.indigo.darken1'
        v.theme.themes.dark.warning = '' # Unallocated
        v.theme.themes.light.warning = ''
        v.theme.themes.dark.anchor = '' # Unallocated
        v.theme.themes.light.anchor = ''

    def load_spectrum_data(self, name, gal_type):
        type_folders = {
            "Sp" : "spirals_spectra",
            "E" : "ellipticals_spectra",
            "Ir" : "irregulars_spectra"
        }

        if not name.endswith(self.name_ext):
            filename = name + self.name_ext
        else:
            filename = name
            name = name[:-len(self.name_ext)]
        spectra_path = Path(__file__).parent / "data" / "spectra"
        folder = spectra_path / type_folders[gal_type]
        path = str(folder / filename)
        data_name = name + '[COADD]'

        # Don't load data that we've already loaded
        dc = self.data_collection
        if data_name not in dc:
            self.app.load_data(path, label=name)
            data = dc[data_name]
            data['lambda'] = 10 ** data['loglam']
            dc.remove(dc[name + '[SPECOBJ]'])
            dc.remove(dc[name + '[SPZLINE]'])
            HubblesLaw.make_data_writeable(data)
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
            HubblesLaw.make_data_writeable(data) 
            dc.append(data)

    def update_student_data(self):
        dc = self.data_collection
        meas_data = dc['student_measurements']
        df = meas_data.to_dataframe()
        df = df[df['distance'].notna() & \
                df['velocity'].notna() & \
                df['angular_size'].notna()]
        df["name"] = df["name"].astype(np.dtype(str))
        main_components = [x.label for x in meas_data.main_components]
        components = { col: list(df[col]) for col in main_components }
        if not all(len(v) > 0 for v in components.values()):
            return

        new_data = Data(label='student_data')
        for col, data in components.items():
            categorical = col in self.categorical_cols
            ctype = CategoricalComponent if categorical else Component
            comp = ctype(np.array(data))
            new_data.add_component(comp, col)
        
        student_data = dc['student_data']
        student_data.update_values_from_data(new_data)
        HubblesLaw.make_data_writeable(student_data)

    @staticmethod
    def prune_none(data):
        indices = set()
        for i in range(data.size):
            if any(data[comp][i] is None for comp in data.main_components):
                indices.add(i)

        keep = [x for x in range(data.size) if x not in indices]
        pruned_components = { comp.label: [data[comp][x] for x in keep] for comp in data.main_components }
        pruned = Data(label=data.label, **pruned_components)
        data.update_values_from_data(pruned)

    @staticmethod
    def make_data_writeable(data):
        for comp in data.main_components:
            data[comp.label].setflags(write=True)

    def galaxy_info(self, galaxy_ids):
        sdss = self.data_collection["SDSS_all_sample_filtered"]
        indices = [i for i in range(sdss.size) if sdss['id'][i] in galaxy_ids]
        components = [x for x in sdss.main_components if x.label != 'id']
        return { sdss['id'][index]: { comp.label: sdss[comp][index] for comp in components } for index in indices }

    def fetch_measurement_data(self, url):
        response = requests.get(url)
        res_json = response.json()
        measurements = res_json["measurements"]
        for measurement in measurements:
            measurement.update(measurement.get("galaxy", {}))
        components = { STATE_TO_MEAS.get(k, k) : [measurement.get(k, None) for measurement in measurements] for k in self.measurement_keys }

        for i, name in enumerate(components["name"]):
            if name.endswith(self.name_ext):
                components["name"][i] = name[:-len(self.name_ext)]
        data = Data(**components)
        return data

    def fetch_data_and_update(self, url, label, prune_none=False, make_writeable=False):
        new_data = self.fetch_measurement_data(url)
        new_data.label = label
        if prune_none:
            HubblesLaw.prune_none(new_data)
        data = self.data_collection[label]
        data.update_values_from_data(new_data)
        if make_writeable:
            HubblesLaw.make_data_writeable(data)

    def fetch_student_data(self):
        student_meas_url = f"{API_URL}/{HUBBLE_ROUTE_PATH}/measurements/{self.student['id']}"
        student_meas_label = "student_measurements"
        self.fetch_data_and_update(student_meas_url, student_meas_label, make_writeable=True)
        self.update_student_data()

    def fetch_class_data(self):
        class_meas_url = f"{API_URL}/{HUBBLE_ROUTE_PATH}/stage-3-data/{self.student['id']}/{self.classroom['id']}"
        class_meas_label = "class_data"
        self.fetch_data_and_update(class_meas_url, class_meas_label, prune_none=True)

    def setup_for_student(self, app_state):
        super().setup_for_student(app_state)
        self.fetch_student_data()
        self.fetch_class_data()


