import ipyvue as v
from cosmicds.utils import load_template
from traitlets import Instance, Bool, Float, Int, observe
from ipywidgets import DOMWidget, widget_serialization

class MeasuringTool(v.VueTemplate):
    template = load_template("measuring_tool.vue", __file__).tag(sync=True)
    widget = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)
    measuring = Bool().tag(sync=True)
    measuredDistance = Float().tag(sync=True)
    angular_distance = Float().tag(sync=True)
    height = Int().tag(sync=True)
    width = Int().tag(sync=True)
    
    def __init__(self, wwt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = wwt
        self.measuring = kwargs.get('measuring', False)
        self.height = self._height_from_pixel_str(self.widget.layout.height or '400px')
        self.width = self._height_from_pixel_str(self.widget.layout.width or '500px')
        
    def reset_canvas(self):
        self.send({"method": "reset", "args": []})

    def _height_from_pixel_str(self, s):
        return int(s[:-2]) # Remove the 'px' from the end

    @observe('measuredDistance')
    def _on_measured_distance_changed(self, change):
        fov = self.widget.get_fov()
        widget_height = self.height
        self.angular_distance = ((change["new"] / widget_height) * fov).value
        
    @observe('measuring')
    def _on_measuring_changed(self, measuring):
        if not measuring["new"]:
            self.reset_canvas()

