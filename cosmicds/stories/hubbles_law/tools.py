from bqplot.marks import Label, Lines
from glue_jupyter.bqplot.common.tools import InteractCheckableTool
from cosmicds.stories.hubbles_law.utils import H_ALPHA_REST_LAMBDA, MG_REST_LAMBDA

class RestWavelengthTool(InteractCheckableTool):

    observed_text = ' (observed)'
    rest_text = ' (rest)'

    def __init__(self, viewer, **kwargs):
        super().__init__(viewer, **kwargs)
        self.showing = False

        self.line = Lines(
            x=[0, 0],
            y=[0, 0],
            line_style='dotted',
            colors=['black'],
            scales={
                'x': self.scales['x'],
                'y': self.scales['y'],
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
                'x': self.scales['x'],
                'y': self.scales['y'],
            }
        )

        self.marks = [self.line, self.label]

    def toggle_showing(self):
        if self.showing:
            self.viewer.figure.marks = [mark for mark in self.viewer.figure.marks if mark not in self.marks]
            self.viewer.observed_label.text = [self.viewer.observed_label.text[0][:-len(self.observed_text)]]
            self.showing = False
        else:
            element = self.viewer.element
            rest = MG_REST_LAMBDA if element == 'Mg-I' else H_ALPHA_REST_LAMBDA
            self.line.x = [rest, rest]
            self.label.x = [rest, rest]
            self.viewer.observed_label.text = [self.viewer.observed_label.text[0] + self.observed_text]
            self.viewer.figure.marks += self.marks
            self.showing = True
