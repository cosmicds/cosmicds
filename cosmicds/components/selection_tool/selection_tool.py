import ipyvue as v
import astropy.units as u

from astropy.table import Table
from astropy.coordinates import SkyCoord
from cosmicds.utils import load_template
from cosmicds.stories.hubbles_law.utils import FULL_FOV, GALAXY_FOV
from ipywidgets import DOMWidget, widget_serialization
from pandas import DataFrame
from pywwt.jupyter import WWTJupyterWidget
from traitlets import Dict, Instance

class SelectionTool(v.VueTemplate):
    template = load_template("selection_tool.vue", __file__, traitlet=True).tag(sync=True)
    widget = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)
    current_galaxy = Dict().tag(sync=True)

    START_COORDINATES = SkyCoord(180 * u.deg, 25 * u.deg, frame='icrs')

    def __init__(self, data, *args, **kwargs):
        self.widget = WWTJupyterWidget(hide_all_chrome=True)
        self.widget.background = 'SDSS: Sloan Digital Sky Survey (Optical)'
        self.widget.foreground = 'SDSS: Sloan Digital Sky Survey (Optical)'
        self.widget.center_on_coordinates(self.START_COORDINATES, instant=False)

        df = data.to_dataframe()
        table = Table.from_pandas(df)
        layer = self.widget.layers.add_table_layer(table)
        layer.size_scale = 50
        layer.color = "#00FF00"
        self.sdss_layer = layer
        self.motions_left = 2
        self.gals_max = kwargs.get("galaxies_max", 5)

        self.selected_data = DataFrame()
        self.selected_layer = None
        self.current_galaxy = {}
        self._on_galaxy_selected = None

        def wwt_cb(wwt, updated):
            print(self.selected_data.shape)
            if 'most_recent_source' not in updated or self.selected_data.shape[1] >= self.gals_max:
                return

            source = wwt.most_recent_source
            galaxy = source["layerData"]
            for k in ["RA", "DEC", "Z"]:
                galaxy[k] = float(galaxy[k])
            self.current_galaxy = galaxy
            fov = min(wwt.get_fov(), GALAXY_FOV)
            self.go_to_galaxy(galaxy["RA"], galaxy["DEC"], fov=fov)
            self.current_galaxy = galaxy

        self.widget.set_selection_change_callback(wwt_cb)

        super().__init__(*args, **kwargs)

    @property
    def on_galaxy_selected(self):
        return self._on_galaxy_selected

    @on_galaxy_selected.setter
    def on_galaxy_selected(self, cb):
        self._on_galaxy_selected = cb

    def vue_select_current_galaxy(self, _args=None):
        self.selected_data = self.selected_data.append(self.current_galaxy, ignore_index=True)
        table = Table.from_pandas(self.selected_data)
        layer = self.widget.layers.add_table_layer(table)
        layer.size_scale = 100
        layer.color = "#FF00FF"
        if self.selected_layer is not None:
            self.widget.layers.remove_layer(self.selected_layer)
        self.selected_layer = layer
        if self._on_galaxy_selected is not None:
            self._on_galaxy_selected(self.current_galaxy)
        self.current_galaxy = {}

    def vue_reset(self, _args=None):
        self.widget.center_on_coordinates(self.START_COORDINATES, fov=FULL_FOV, instant=True)
        self.current_galaxy = {}

    def go_to_galaxy(self, ra, dec, fov=GALAXY_FOV):
        coordinates = SkyCoord(ra * u.deg, dec * u.deg, frame='icrs')
        instant = self.motions_left <= 0
        if not instant:
            self.motions_left -= 1
        self.widget.center_on_coordinates(coordinates, fov=fov, instant=instant)
