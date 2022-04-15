import ipyvuetify as v
from cosmicds.utils import load_template
from glue_jupyter.state_traitlets_helpers import GlueState
from traitlets import Float, Bool

class ReflectVelocityCalc(v.VuetifyTemplate):
    template = load_template("reflect_velocity_calc.vue", __file__, traitlet=True).tag(sync=True)
    state = GlueState().tag(sync=True)
    print("this is a test")

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)
    
    def vue_validate_python(self, args):
        print("We're validating with Python!")
        result = True
        print(self.state)
        #expected=[3,5]
        expected = [self.state.lambda_rest, self.state.lambda_obs]
        print("python expected", expected)
        #expected = [self.state.expected_1, self.state.expected_2]
        answers = [float(x) for x in args["answers"]]
        for ans, exp in zip(answers, expected):
            if ans != exp:
                result = False
                break
        print(f"Are answers correct? {result}")
        return result