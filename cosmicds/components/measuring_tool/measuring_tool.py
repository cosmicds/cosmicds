import os
import ipyvue as v
from astropy.coordinates import Angle
from astropy.coordinates.sky_coordinate import SkyCoord
import astropy.units as u
from cosmicds.utils import load_template
from traitlets import Instance, Bool, Float, Int, Unicode, observe
from ipywidgets import DOMWidget, widget_serialization

def angle_to_json(angle, _widget):
    return {
        "value": angle.value,
        "unit": angle.unit.name
    }

def angle_from_json(jsn, _widget):
    return jsn["value"] * u.Unit(jsn["unit"])

class MeasuringTool(v.VueTemplate):
    template = load_template("measuring_tool.vue", __file__).tag(sync=True)
    widget = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)
    measuring = Bool().tag(sync=True)
    measuredDistance = Float().tag(sync=True)
    angular_size = Instance(Angle).tag(sync=True, to_json=angle_to_json, from_json=angle_from_json)
    angular_height = Instance(Angle).tag(sync=True, to_json=angle_to_json, from_json=angle_from_json)
    height = Int().tag(sync=True)
    width = Int().tag(sync=True)
    view_changing = Bool().tag(sync=True)
    _ra = Angle(0 * u.deg)
    _dec = Angle(0 * u.deg)

    def __init__(self, wwt, *args, **kwargs):
        self.widget = wwt
        self.measuring = kwargs.get('measuring', False)
        self.angular_size = Angle(0, u.deg)
        self.angular_height = Angle(60, u.deg)
        self.widget._set_message_type_callback('wwt_view_state', self._handle_view_message)
        super().__init__(*args, **kwargs)

    def reset_canvas(self):
        self.send({"method": "reset", "args": []})

    def _height_from_pixel_str(self, s):
        return int(s[:-2]) # Remove the 'px' from the end

    @observe('measuredDistance')
    def _on_measured_distance_changed(self, change):
        fov = self.widget.get_fov()
        widget_height = self._height_from_pixel_str(self.widget.layout.height)
        self.angular_size = Angle(((change["new"] / widget_height) * fov))

    @observe('measuring')
    def _on_measuring_changed(self, measuring):
        if not measuring["new"]:
            self.reset_canvas()

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
