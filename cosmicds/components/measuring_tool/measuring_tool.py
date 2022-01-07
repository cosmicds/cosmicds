import astropy.units as u
import ipyvue as v
from cosmicds.utils import load_template
from traitlets import Instance, Bool, Float, Int, Unicode, observe
from ipywidgets import DOMWidget, widget_serialization

class MeasuringTool(v.VueTemplate):
    template = load_template("measuring_tool.vue", __file__).tag(sync=True)
    widget = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)
    measuring = Bool().tag(sync=True)
    measuredDistance = Float().tag(sync=True)
    angular_distance = Float().tag(sync=True)
    angular_distance_str = Unicode("0°").tag(sync=True)
    angular_height_str = Unicode("60°").tag(sync=True)
    height = Int().tag(sync=True)
    width = Int().tag(sync=True)
    
    def __init__(self, wwt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = wwt
        self.measuring = kwargs.get('measuring', False)
        self.widget._set_message_type_callback('wwt_view_state', self._on_fov_change)
        
    def reset_canvas(self):
        self.send({"method": "reset", "args": []})

    def _height_from_pixel_str(self, s):
        return int(s[:-2]) # Remove the 'px' from the end

    @observe('measuredDistance')
    def _on_measured_distance_changed(self, change):
        fov = self.widget.get_fov()
        widget_height = self._height_from_pixel_str(self.widget.layout.height)
        angular_dist = ((change["new"] / widget_height) * fov)
        self.angular_distance = angular_dist.value # In degrees
        self.angular_distance_str = self.format_angle(angular_dist)
        
    @observe('measuring')
    def _on_measuring_changed(self, measuring):
        if not measuring["new"]:
            self.reset_canvas()

    def _on_fov_change(self, wwt, _updated):
        fov = self.widget.get_fov().to(u.deg)
        self.angular_height = fov
        self.angular_height_str = self.format_angle(fov)

    def format_angle(self, angle):
        angle_deg = angle.to(u.deg)
        if angle_deg.value >= 1:
            return f"{angle_deg.value:.2f}°"

        angle_min = angle_deg.to(u.arcmin)
        if angle_min.value >= 1:
            return f"{angle_min.value:.2f}′"
        
        angle_asec = angle_min.to(u.arcsec)
        return f"{angle_asec.value:.2f}″"

