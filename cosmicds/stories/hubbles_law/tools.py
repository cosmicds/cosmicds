from bqplot.marks import Label, Lines
from glue.config import viewer_tool
from glue_jupyter.bqplot.common.tools import InteractCheckableTool
from cosmicds.stories.hubbles_law.utils import H_ALPHA_REST_LAMBDA, MG_REST_LAMBDA

@viewer_tool
class RestWavelengthTool(InteractCheckableTool):

    tool_id = "bqplot:restwave"
    action_text = "Show rest wavelength"
    tool_tip = "Toggle display of the rest wavelength line"

    observed_text = ' (observed)'
    rest_text = ' (rest)'

    def __init__(self, viewer, **kwargs):
        super().__init__(viewer, **kwargs)
        self.showing = False

        scales = self.viewer.scales
        self.line = Lines(
            x=[0, 0],
            y=[0, 0],
            line_style='dotted',
            colors=['black'],
            scales={
                'x': scales['x'],
                'y': scales['y'],
            }
        )

        self.label = Label(
            text=[],
            x=[],
            y=[],
            x_offset=-5,
            opacities=[0.7],
            colors=['black'],
            scales={
                'x': scales['x'],
                'y': scales['y'],
            }
        )

        self.marks = [self.line, self.label]

        self.viewer.scale_y.observe(self._on_view_change, names=['min', 'max'])

    def toggle_showing(self):
        self.showing = not self.showing
        self.user_line.visible = not self.showing
        self.user_line_label.visible = not self.showing
        if self.showing:
            element = self.viewer.element
            rest = MG_REST_LAMBDA if element == 'Mg-I' else H_ALPHA_REST_LAMBDA
            self.line.x = [rest, rest]
            self.label.x = [rest, rest]
            self.viewer.visible_wavelength_line.text = [self.viewer.element + self.rest_text]
            self.viewer.element_label.text = [self.viewer.observed_label.text[0] + self.observed_text]
            self.viewer.figure.marks += self.marks
        else:
            self.viewer.figure.marks = [mark for mark in self.viewer.figure.marks if mark not in self.marks]
            self.viewer.visible_wavelength_line.text = [self.viewer.element]
            self.viewer.element_label.text = [self.viewer.observed_label.text[0][:-len(self.observed_text)]]

    def _on_view_change(self, event=None):
        scale = self.viewer.scales['y']
        
        if scale.min is None or scale.max is None:
            return
        
        ymin, ymax = scale.min, scale.max
        top_label_position = ymax * 0.96
        restwave_line_bounds = [ymin, ymax * 0.93]
        self.line.y = restwave_line_bounds
        self.label.y = [top_label_position]
