import ipyvuetify as v
from cosmicds.utils import load_template
from glue_jupyter.state_traitlets_helpers import GlueState
from traitlets import Float, Bool, Int, Unicode, List

class DopplerCalc(v.VuetifyTemplate):
    template = Unicode().tag(sync=True)
    step = Int(0).tag(sync=True)
    length = Int(6).tag(sync=True)
    currentTitle = Unicode("").tag(sync=True)
    state = GlueState().tag(sync=True)
    failedValidation4 = Bool(False).tag(sync=True)
    failedValidation5 = Bool(False).tag(sync=True)
    interactSteps5 = List([3,4]).tag(sync=True)
    maxStepCompleted5 = Int(0).tag(sync=True)
    studentc = Float(0).tag(sync=True)
    student_vel_calc = Bool(False).tag(sync=True) # stage_one.py listens for whether this value changes

    _titles = [
        "Doppler Calculation",
        "Doppler Calculation",
        "Doppler Calculation",
        "Reflect on Your Result",
        "Enter Speed of Light",
        "Your Galaxy's Velocity",
    ]
    _default_title = "Doppler Calculation"    

    def __init__(self, filename, path, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)
        self.template = load_template(filename, path)
        self.currentTitle = self._default_title

        def update_title(change):
            index = change["new"]
            if index in range(len(self._titles)):
                self.currentTitle = self._titles[index]
            else:
                self.currentTitle = self._default_title

        self.observe(update_title, names=["step"])


