import json
import requests
from random import randint

from cosmicds.phases import Stage
from cosmicds.utils import API_URL, CDSJSONEncoder
from cosmicds.stories.hubbles_law.utils import HUBBLE_ROUTE_PATH

class HubbleStage(Stage):

    _measurement_mapping = {
        "measwave": "obs_wave_value",
        "restwave": "rest_wave_value",
        "velocity": "velocity_value",
        "distance": "est_dist_value",
        "name": "galaxy_name",
        "student_id": "student_id",
        "angular_size" : "ang_size_value"
    }

    _units = {
        "rest_wave_unit": "angstrom",
        "obs_wave_unit": "angstrom",
        "est_dist_unit": "Mpc",
        "velocity_unit": "km / s",
        "ang_size_unit": "arcsecond"
    }
    
    @classmethod
    def _map_key(cls, key):
        return cls._measurement_mapping.get(key, key)

    def _prepare_measurement(self, measurement):
        prepared = { HubbleStage._map_key(k) : measurement.get(k, None) for k in HubbleStage._measurement_mapping.keys() }
        prepared.update(HubbleStage._units)
        prepared["student_id"] = self.app_state.student["id"]
        prepared = json.loads(json.dumps(prepared, cls=CDSJSONEncoder))
        return prepared

    def submit_measurement(self, measurement):
        prepared = self._prepare_measurement(measurement)
        requests.put(f"{API_URL}/{HUBBLE_ROUTE_PATH}/sample-measurement", json=prepared)

    def remove_measurement(self, galaxy_name):
        user = self.app_state.student
        if user.get("id", None) is not None:
            requests.delete(f"{API_URL}/{HUBBLE_ROUTE_PATH}/sample-measurement/{user['id']}")

    def _replace_galaxy_at_index(self, index):
        sdss_data = self.get_data("Sample_Galaxy")
        components = [x.label for x in sdss_data.main_components]
        meas_data = self.get_data("student_measurements")
        student_comps = [x.label for x in meas_data.main_components]
        while True:
            sdss_index = randint(0, sdss_data.size-1)
            galaxy = { c: sdss_data[c][sdss_index] for c in components if c in student_comps }
            if galaxy['name'] not in meas_data['name']:
                break
        values = { c: galaxy.get(c, None) for c in student_comps }
        self.update_data_values("student_measurements", values, index)    
        return galaxy

    def update_data_value(self, dc_name, comp_name, value, index):
        super().update_data_value(dc_name, comp_name, value, index)

        if self.app_state.update_db \
            and dc_name == "student_measurements" \
            and comp_name in HubbleStage._measurement_mapping.keys():

            data = self.data_collection[dc_name]
            measurement = { comp.label: data[comp][index] for comp in data.main_components }
            self.submit_measurement(measurement)

    def update_data_values(self, dc_name, values, index):
        super().update_data_values(dc_name, values, index)

        if self.app_state.update_db \
            and dc_name == "student_measurements":

            data = self.data_collection[dc_name]
            measurement = { comp.label: data[comp][index] for comp in data.main_components if comp.label in HubbleStage._measurement_mapping.keys() }
            self.submit_measurement(measurement)

    def add_data_values(self, dc_name, values):
        super().add_data_values(dc_name, values)

        if self.app_state.update_db and dc_name == "student_measurements":
            self.submit_measurement(values)
