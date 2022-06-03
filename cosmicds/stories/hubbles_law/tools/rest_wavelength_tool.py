from bqplot.marks import Label, Lines
from echo import add_callback, CallbackProperty
from glue.config import viewer_tool
from glue.viewers.common.tool import CheckableTool
from cosmicds.stories.hubbles_law.utils import H_ALPHA_REST_LAMBDA, MG_REST_LAMBDA

@viewer_tool
class RestWavelengthTool(CheckableTool):

    tool_id = "hubble:restwave"
    action_text = "Show rest wavelength"
    tool_tip = "Toggle display of the rest wavelength line"
    mdi_icon = "mdi-lambda"

    observed_text = ' (observed)'
    rest_text = ' (rest)'

    lambda_used = CallbackProperty(False)

    def __init__(self, viewer, **kwargs):
        super().__init__(viewer, **kwargs)
        self.active = False

        scales = self.viewer.scales
        self.line = Lines(
            x=[0, 0],
            y=[0, 0],
            line_style='dotted',
            opacities=[0.7],
            colors=['black'],
            scales={
                'x': scales['x'],
                'y': scales['y'],
            })

        self.label = Label(
            text=[""],
            x=[],
            y=[],
            x_offset=-5,
            opacities=[0.7],
            colors=['black'],
            scales={
                'x': scales['x'],
                'y': scales['y'],
            })

        self.marks = [self.line, self.label]

        self.viewer.scale_y.observe(self._on_view_change, names=['min', 'max'])
        add_callback(self.viewer.state, 'y_min', self._on_view_change)
        add_callback(self.viewer.state, 'y_max', self._on_view_change)
        self._on_view_change()

    def activate(self):
        rest = MG_REST_LAMBDA if self.viewer.element == 'Mg-I' else H_ALPHA_REST_LAMBDA
        self.line.x = [rest, rest]
        self.label.x = [rest, rest]
        self.label.text = [self.viewer.element + self.rest_text]
        self.viewer.element_label.text = [self.viewer.element + self.observed_text]
        self.active = True
        self._on_view_change()
        self.viewer.figure.marks = self.viewer.figure.marks + self.marks
        self.lambda_used = True

    def deactivate(self):
        self.viewer.figure.marks = [mark for mark in self.viewer.figure.marks if mark not in self.marks]
        self.viewer.element_label.text = [self.viewer.element]
        self.active = False

    def _on_view_change(self, event=None):
        if not self.active:
            return
        scale = self.viewer.scales['y']
        ymin, ymax = scale.min, scale.max
        if ymin is None or ymax is None:
            return
        self.line.y = [ymin, ymax * 0.93]
        self.label.y = [ymax * 0.96]
