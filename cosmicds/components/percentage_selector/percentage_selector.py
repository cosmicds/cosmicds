from ipyvuetify import VuetifyTemplate
from numpy import percentile
from traitlets import Float, Int, List, observe

from glue.core.subset import RangeSubsetState

from ...utils import load_template

class PercentageSelector(VuetifyTemplate):
    
    template = load_template("percentage_selector.vue", __file__, traitlet=True).tag(sync=True)
    options = List([50, 68, 95]).tag(sync=True)
    selected = Int().tag(sync=True)
    selected_min = Float().tag(sync=True)
    selected_max = Float().tag(sync=True)

    def __init__(self, viewer, data, component_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewer = viewer
        self.glue_data = data
        self.component_id = component_id
        self._bins = kwargs.get("bins", None)
        if "options" in kwargs:
            self.options = kwargs.get("options")
        self.subset_label = kwargs.get("subset_label", None)
        self.subset_group = kwargs.get("subset_group", False)
        self.transform = kwargs.get("transform", None)
        self._subset = None

    @property
    def bins(self):
        if self._bins is not None:
            return self._bins
        if hasattr(self.viewer.state, "bins"):
            return self.viewer.state.bins
        return None

    @observe('selected')
    def _update_subset(self, change):
        selected = change["new"]
        around_median = selected / 2
        bottom_percent = 50 - around_median
        top_percent = 50 + around_median
        data = self.glue_data[self.component_id]
        bottom = percentile(data, bottom_percent, method="nearest")
        top = percentile(data, top_percent, method="nearest")
        state = RangeSubsetState(bottom, top, self.component_id)
        if self.bins is not None:
            print(self.bins)
            bottom = next((x for x in self.bins if x > bottom), bottom)
            top = next((x for x in self.bins if x > top), top)
        if self.transform:
            bottom = self.transform(bottom)
            top = self.transform(top)
        self.selected_min = bottom
        self.selected_max = top
        if self._subset is None:
            kwargs = { "label": self.subset_label } if self.subset_label else {}
            if self.subset_group:
                self._subset = self.viewer.session.data_collection.new_subset_group(state, **kwargs)
            else:
                self._subset = self.glue_data.new_subset(state, **kwargs)
                self.viewer.add_subset(self._subset)
        else:
            self._subset.subset_state = state
