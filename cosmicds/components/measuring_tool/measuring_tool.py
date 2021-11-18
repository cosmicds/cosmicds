import os
import ipyvue as v
from cosmicds.utils import load_template
from traitlets import Instance, Bool, Float, observe
from ipywidgets import DOMWidget, widget_serialization

class MeasuringTool(v.VueTemplate):
    template = load_template("measuring_tool.vue", __file__).tag(sync=True)
    widget = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)
    measuring = Bool().tag(sync=True)
    measuredDistance = Float().tag(sync=True)
    angular_distance = Float().tag(sync=True)
    
    def __init__(self, wwt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = wwt
        self.measuring = kwargs.get('measuring', False)
        
    def reset_canvas(self):
        self.send({"method": "reset", "args": []})
        
    @property
    def angular_distance(self):
        fov = self.widget.get_fov()
        widget_height = int(self.widget.layout.height[:-2])
        return (self.measuredDistance / widget_height) * fov
        
    @observe('measuring')
    def _on_measuring_changed(self, measuring):
        if not measuring["new"]:
            self.reset_canvas()

