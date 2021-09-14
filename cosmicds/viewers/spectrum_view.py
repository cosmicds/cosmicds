from glue_jupyter.bqplot.profile import BqplotProfileView
from bqplot.marks import Lines
from bqplot import Label

__all__ = ['SpectrumView']


class SpectrumView(BqplotProfileView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.user_line = Lines(
            x=[0, 0], 
            y=[0, 0], 
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            })
        
        self.user_line_label = Label(
            text=[""], 
            x=[], 
            y=[],
            x_offset=10,
            y_offset=10,
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
            })
        
        self.figure.marks += [self.user_line, self.user_line_label]
        
        self.add_event_callback(self._on_mouse_moved, events=['mousemove'])
        self.scale_y.observe(self._on_view_change, names=['min', 'max'])
        
    def _on_view_change(self, event):
        scales = self.scales['y']
        
        if scales.min is None or scales.max is None:
            return
        
        self.user_line.y = [self.scales['y'].min, self.scales['y'].max]
        self.user_line_label.x = [self.user_line.x[0]]
        self.user_line_label.y = [self.user_line.y[1]]
        
    def _on_mouse_moved(self, event):
        new_x = event['domain']['x']
        self.user_line_label.text = [f"{new_x:.2f}"]
        
        self.user_line.x = [new_x - 1, new_x + 1]
        self.user_line_label.x = [new_x - 1, new_x + 1]
