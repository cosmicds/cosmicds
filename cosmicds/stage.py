import json

import ipyvuetify as v
import requests
from cosmicds.components import Table
from cosmicds.phases import Stage
from cosmicds.utils import API_URL, CDSJSONEncoder
from echo import add_callback

from .data_management import MEAS_TO_STATE, UNITS_TO_STATE
from .utils import HUBBLE_ROUTE_PATH


class HubbleStage(Stage):

    def __init__(self, session, story_state, app_state, *args, **kwargs):
        super().__init__(session, story_state, app_state, *args, **kwargs)

        # Respond to dark/light mode change
        add_callback(self.app_state, 'dark_mode', self._on_dark_mode_change)

    @staticmethod
    def _map_key(key):
        return MEAS_TO_STATE.get(key, key)

    def _prepare_measurement(self, measurement):
        prepared = {HubbleStage._map_key(k): measurement.get(k, None) for k in
                    MEAS_TO_STATE.keys()}
        prepared.update(UNITS_TO_STATE)
        prepared["student_id"] = self.app_state.student["id"]
        ext = ".fits"
        if not prepared["galaxy_name"].endswith(ext):
            prepared["galaxy_name"] += ext
        prepared = json.loads(json.dumps(prepared, cls=CDSJSONEncoder))
        return prepared

    def submit_measurement(self, measurement):
        prepared = self._prepare_measurement(measurement)
        requests.put(f"{API_URL}/{HUBBLE_ROUTE_PATH}/submit-measurement",
                     json=prepared)

    def remove_measurement(self, galaxy_name):
        name = str(galaxy_name)
        condition = lambda x: x == name
        if not galaxy_name.endswith(".fits"):
            galaxy_name += ".fits"
        self.remove_data_values("student_measurements", "name", condition,
                                single=True)
        user = self.app_state.student
        if user.get("id", None) is not None:
            requests.delete(
                f"{API_URL}/{HUBBLE_ROUTE_PATH}/measurement/{user['id']}/{galaxy_name}")

    def update_data_value(self, dc_name, comp_name, value, index):
        super().update_data_value(dc_name, comp_name, value, index)

        if dc_name != "student_measurements":
            return

        if self.app_state.update_db \
                and comp_name in MEAS_TO_STATE.keys():
            data = self.data_collection[dc_name]
            measurement = {comp.label: data[comp][index] for comp in
                           data.main_components}
            self.submit_measurement(measurement)

    def add_data_values(self, dc_name, values):
        super().add_data_values(dc_name, values)
        self.story_state.update_student_data()

        if self.app_state.update_db and dc_name == "student_measurements":
            self.submit_measurement(values)

    def table_selected_color(self, dark):
        theme = v.theme.themes.dark if dark else v.theme.themes.light
        return theme.info

    def _on_dark_mode_change(self, dark):
        color = self.table_selected_color(dark)
        for widget in self.widgets.values():
            if isinstance(widget, Table):
                widget.selected_color = color
