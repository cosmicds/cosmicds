from ipyvuetify import VuetifyTemplate
from traitlets import Int, observe

from ...utils import load_template

class PercentageSelector(VuetifyTemplate):
    
    template = load_template("percentage_selector.vue", __file__, traitlet=True).tag(sync=True)
    selected = Int().tag(sync=True)

    def __init__(self, data, component_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
        self.component_id = component_id
        self._subset = None

    @observe('selected')
    def _update_subset(self, change):
        selected = change["new"]
        around_median = selected / 2
        bottom_percent = 50 - around_median
        top_percent = 50 + around_median
        bottom = self.data.compute_statistic('percentile', self.component_id, percentile=bottom_percent)
        top = self.data.compute_statistic('percentile', self.component_id, percentile=top_percent)
        state = self.data[self.component_id.label] >= bottom & self.data[self.component_id.label] <= top
        if self._subset is None:
            self._subset = self.data.new_subset(state)
        else:
            self._subset.subset_state = state
