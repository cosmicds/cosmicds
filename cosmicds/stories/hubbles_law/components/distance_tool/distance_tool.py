import json
from math import floor
import requests

import ipyvue as v
from astropy.coordinates import Angle, SkyCoord
import astropy.units as u
from cosmicds.utils import RepeatedTimer, load_template, API_URL
from cosmicds.stories.hubbles_law.utils import GALAXY_FOV, HUBBLE_ROUTE_PATH, angle_to_json, angle_from_json
from pywwt.jupyter import WWTJupyterWidget
from traitlets import Instance, Bool, Float, Int, Dict, Unicode, observe
from ipywidgets import DOMWidget, widget_serialization
from datetime import datetime
from glue_jupyter.state_traitlets_helpers import GlueState

class DistanceTool(v.VueTemplate):
    template = load_template("distance_tool.vue", __file__, traitlet=True).tag(sync=True)
    widget = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)
    measuring = Bool().tag(sync=True)
    measuredDistance = Float().tag(sync=True)
    angular_size = Instance(Angle).tag(sync=True, to_json=angle_to_json, from_json=angle_from_json)
    angular_height = Instance(Angle).tag(sync=True, to_json=angle_to_json, from_json=angle_from_json)
    height = Int().tag(sync=True)
    width = Int().tag(sync=True)
    view_changing = Bool(False).tag(sync=True)
    measuring_allowed = Bool(False).tag(sync=True)
    fov_text = Unicode().tag(sync=True)
    flagged = Bool(False).tag(sync=True)
    state = GlueState().tag(sync=True)
    _ra = Angle(0 * u.deg)
    _dec = Angle(0 * u.deg)

    UPDATE_TIME = 1 #seconds

    def __init__(self, state, *args, **kwargs):
        self.state = state
        self.widget = WWTJupyterWidget(hide_all_chrome=True)
        self._setup_widget()
        self.measuring = kwargs.get('measuring', False)
        self.angular_size = Angle(0, u.deg)
        self.angular_height = Angle(60, u.deg)
        self.widget._set_message_type_callback('wwt_view_state', self._handle_view_message)
        self.last_update = datetime.now()
        self._rt = RepeatedTimer(self.UPDATE_TIME, self._check_view_changing)
        self.update_text()
        super().__init__(*args, **kwargs)

    def _setup_widget(self):
        # Temp update to set background to SDSS. Once we remove galaxies without SDSS WWT tiles from the catalog, make background DSS again, and set wwt.foreground_opacity = 0, per Peter Williams.
        self.widget.background = 'SDSS: Sloan Digital Sky Survey (Optical)'
        self.widget.foreground = 'SDSS: Sloan Digital Sky Survey (Optical)'

    def reset_canvas(self):
        self.send({"method": "reset", "args": []})

    def update_text(self):
        self.send({"method": "update_text", "args": []})

    def _height_from_pixel_str(self, s):
        return int(s[:-2]) # Remove the 'px' from the end

    # We aren't always guaranteed to get an update from the WWT viewer
    # so every second, if the view is marked as changing, 
    # we check when the last update that we got is
    # If it's more than a second old, mark the view as not changing
    def _check_view_changing(self):
        if self.view_changing:
            delta = datetime.now() - self.last_update
            if delta.total_seconds() >= self.UPDATE_TIME:
                self.view_changing = False

    def vue_toggle_measuring(self, _args=None):
        self.measuring = not self.measuring
        self.state.ruler_clicked = True

    @observe('measuredDistance')
    def _on_measured_distance_changed(self, change):
        fov = self.widget.get_fov()
        widget_height = self._height_from_pixel_str(self.widget.layout.height)
        self.angular_size = Angle(((change["new"] / widget_height) * fov))

    @observe('measuring')
    def _on_measuring_changed(self, measuring):
        if not measuring["new"]:
            self.reset_canvas()

    @observe("angular_height")
    def _on_fov_change(self, change):
        d, m, s = change["new"].dms
        m = m + s/60
        d = d + m/60
        s = int(s)
        if d > 9.95: #to avoid edge case where you can get 10 between 10 and 11 and 10.0 from 9.95-10
            self.fov_text = f"{d:.0f}°"
        elif d > 0.99: #to avoid edge case where you can get 60.0 arcmin from 59.5-59.9 arcmin
            self.fov_text = f"{d:.1f}°"
        elif m > 9.95:
            self.fov_text = f"{m:.0f}'"
        elif m > 0.99:
            self.fov_text = f"{m:.1f}'"
        else:
            self.fov_text = f"{s}\""
        self.update_text()

    def _handle_view_message(self, wwt, _updated):
        fov = Angle(self.widget.get_fov())
        center = self.widget.get_center()
        ra = Angle(center.ra)
        dec = Angle(center.dec)
        changing = not u.allclose([fov, ra, dec], [self.angular_height, self._ra, self._dec])
        self.angular_height = fov
        self._ra = ra
        self._dec = dec
        self.view_changing = changing
        self.last_update = datetime.now()

    def go_to_location(self, ra, dec, fov=GALAXY_FOV):
        coordinates = SkyCoord(ra * u.deg, dec * u.deg, frame='icrs')
        self.widget.center_on_coordinates(coordinates, fov=fov, instant=True)

    @observe('flagged')
    def mark_galaxy_bad(self, change):
        if not change["new"]:
            return
        galaxy = self.state.galaxy
        if galaxy["id"]:
            data = { "galaxy_id" : int(galaxy["id"]) }
        else:
            name = galaxy["name"]
            if not name.endswith(".fits"):
                name += ".fits"
            data = { "galaxy_name" : name }
        requests.post(f"{API_URL}/{HUBBLE_ROUTE_PATH}/mark-tileload-bad", json=data)
