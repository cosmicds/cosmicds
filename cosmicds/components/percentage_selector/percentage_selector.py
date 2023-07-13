from ipyvuetify import VuetifyTemplate
from numpy import array, percentile
from traitlets import Float, Int, List, Unicode, observe

from glue.core import Data
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

    _deselected_color = "#D3D3D3"

    # Note: we pass in the data, rather than the layer itself,
    # to deal with cases where, for either setup or story reasons,
    # the layer doesn't exist in the viewer when we have to create
    # this component (which will be in the stage initializer)
    def __init__(self, viewer, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewer = viewer
        self.glue_data = data
        self._bins = kwargs.get("bins", None)
        if "options" in kwargs:
            self.options = kwargs["options"]
        self.subset_label = kwargs.get("subset_label", None)
        self.subset_group = kwargs.get("subset_group", False)
        self.lower_transform = kwargs.get("lower_transform", None)
        self.upper_transform = kwargs.get("upper_transform", None)
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
            kwargs = { "color": self.color, "alpha": 1 }
            if self.subset_label:
                kwargs["label"] = self.subset_label
            if self.subset_group:
                self.subset = self.viewer.session.data_collection.new_subset_group(state, **kwargs)
            else:
                self.subset = self.glue_data.new_subset(state, **kwargs)
                self.viewer.add_subset(self.subset)
        else:
            self.subset.subset_state = state

    @property
    def layer(self):
        return self.viewer.layer_artist_for_data(self.glue_data)

    @observe('selected')
    def _update(self, change):
        if self.layer is None:
            return
        selected = change["new"]
        if selected is None:
            state = array([False for _ in range(self.glue_data.size)])
            self.layer.state.color = self.color
            self._update_subset(state)
            return

        self.layer.state.color = self._deselected_color
        around_median = selected / 2
        bottom_percent = 50 - around_median
        top_percent = 50 + around_median
        component_id = self.viewer.state.x_att
        data = self.glue_data[component_id]
        bottom = percentile(data, bottom_percent, method="nearest")
        top = percentile(data, top_percent, method="nearest")
        state = RangeSubsetState(bottom, top, component_id)
        if self.bins is not None:
            bottom = next((x for x in self.bins if x > bottom), bottom)
            top = next((x for x in self.bins if x > top), top)
        if self.lower_transform is not None:
            bottom = self.lower_transform(bottom)
        if self.upper_transform is not None:
            top = self.upper_transform(top)
        self.selected_min = bottom
        self.selected_max = top
        self._update_subset(state)
