from ipyvuetify import VuetifyTemplate
from numpy import array, percentile
from traitlets import Float, Int, List, Unicode, observe

from glue.core.subset import RangeSubsetState

from ...utils import load_template

class PercentageSelector(VuetifyTemplate):
    
    template = load_template("percentage_selector.vue", __file__, traitlet=True).tag(sync=True)
    color = Unicode("#1e90ff").tag(sync=True)
    options = List([50, 68, 95]).tag(sync=True)
    selected = Int(allow_none=True).tag(sync=True)
    selected_min = Float().tag(sync=True)
    selected_max = Float().tag(sync=True)
    unit = Unicode().tag(sync=True)
    was_selected = Int(allow_none=True).tag(sync=True)

    def __init__(self, viewer, data, component_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewer = viewer
        self.glue_data = data
        self.component_id = component_id
        self._bins = kwargs.get("bins", None)
        if "options" in kwargs:
            self.options = kwargs["options"]
        if "color" in kwargs:
            self.color = kwargs["color"]
        self.subset_label = kwargs.get("subset_label", None)
        self.subset_group = kwargs.get("subset_group", False)
        self.transform = kwargs.get("transform", None)
        self.subset = None
        if "unit" in kwargs:
            self.unit = kwargs["unit"]

    @property
    def bins(self):
        if self._bins is not None:
            return self._bins
        if hasattr(self.viewer.state, "bins"):
            return self.viewer.state.bins
        return None

    def _update_subset(self, state):
        if self.subset is None:
            kwargs = { "color": self.color }
            if self.subset_label:
                kwargs["label"] = self.subset_label
            if self.subset_group:
                self.subset = self.viewer.session.data_collection.new_subset_group(state, **kwargs)
            else:
                self.subset = self.glue_data.new_subset(state, **kwargs)
                self.viewer.add_subset(self.subset)
        else:
            self.subset.subset_state = state

    @observe('selected')
    def _update(self, change):
        selected = change["new"]
        if selected is None:
            state = array([False for _ in range(self.glue_data.size)])
            self._update_subset(state)
            return

        around_median = selected / 2
        bottom_percent = 50 - around_median
        top_percent = 50 + around_median
        data = self.glue_data[self.component_id]
        bottom = percentile(data, bottom_percent, method="nearest")
        top = percentile(data, top_percent, method="nearest")
        state = RangeSubsetState(bottom, top, self.component_id)
        if self.bins is not None:
            bottom = next((x for x in self.bins if x > bottom), bottom)
            top = next((x for x in self.bins if x > top), top)
        if self.transform:
            bottom = self.transform(bottom)
            top = self.transform(top)
        self.selected_min = bottom
        self.selected_max = top
        self._update_subset(state)
