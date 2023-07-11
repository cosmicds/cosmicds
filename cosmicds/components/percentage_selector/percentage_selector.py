from ipyvuetify import VuetifyTemplate
from traitlets import Int, List, observe

from glue.core.subset import RangeSubsetState

from ...utils import load_template

class PercentageSelector(VuetifyTemplate):
    
    template = load_template("percentage_selector.vue", __file__, traitlet=True).tag(sync=True)
    options = List([50, 68, 95]).tag(sync=True)
    selected = Int().tag(sync=True)

    def __init__(self, viewer, data, component_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewer = viewer
        self.glue_data = data
        self.component_id = component_id
        self.subset_label = kwargs.get("subset_label", None)
        self.subset_group = kwargs.get("subset_group", False)
        self._subset = None

    @observe('selected')
    def _update_subset(self, change):
        selected = change["new"]
        around_median = selected / 2
        bottom_percent = 50 - around_median
        top_percent = 50 + around_median
        bottom = self.glue_data.compute_statistic('percentile', self.component_id, percentile=bottom_percent)
        top = self.glue_data.compute_statistic('percentile', self.component_id, percentile=top_percent)
        state = RangeSubsetState(bottom, top, self.component_id)
        if self._subset is None:
            kwargs = { "label": self.subset_label } if self.subset_label else {}
            if self.subset_group:
                self._subset = self.viewer.session.data_collection.new_subset_group(state, **kwargs)
            else:
                self._subset = self.glue_data.new_subset(state, **kwargs)
                self.viewer.add_subset(self._subset)
                print(self._subset)
                print(self.viewer.layers)
        else:
            self._subset.subset_state = state
