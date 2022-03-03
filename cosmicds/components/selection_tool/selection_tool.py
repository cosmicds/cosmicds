import ipyvue as v
import astropy.units as u

from astropy.table import Table
from astropy.coordinates import SkyCoord
from cosmicds.utils import load_template
from ipywidgets import DOMWidget, widget_serialization
from pandas import DataFrame
from pywwt.jupyter import WWTJupyterWidget
from traitlets import Instance

class SelectionTool(v.VueTemplate):
    template = load_template("selection_tool.vue", __file__).tag(sync=True)
    widget = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)

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

        self.selected_data = DataFrame()
        self.selected_layer = None
        self._on_galaxy_selected = None

        def wwt_cb(wwt, updated):
            if 'most_recent_source' not in updated:
                return

            source = wwt.most_recent_source
            galaxy = source["layerData"]

            self.selected_data.append(galaxy)
            table = Table.from_pandas(df)
            layer = self.widget.layers.add_table_layer(table)
            layer.size_scale = 100
            layer.color = "#FF00FF"
            if self.selected_layer is not None:
                self.widget.layers.remove_layer(self.selected_layer)
            self.selected_layer = layer

            if self._on_galaxy_selected:
                self._on_galaxy_selected(galaxy)

        self.widget.set_selection_change_callback(wwt_cb)

        super().__init__(*args, **kwargs)

    def on_galaxy_selected(self, cb):
        self._on_galaxy_selected = cb
