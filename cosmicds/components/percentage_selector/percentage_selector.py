from ipyvuetify import VuetifyTemplate
from numpy import array, percentile
from traitlets import Float, Int, List, Unicode, observe

from glue.core.subset import RangeSubsetState

from ...utils import load_template

class PercentageSelector(VuetifyTemplate):
    
    template = load_template("percentage_selector.vue", __file__, traitlet=True).tag(sync=True)
    radio_color = Unicode("#1e90ff").tag(sync=True)
    options = List([50, 68, 95]).tag(sync=True)
    selected = Int(None, allow_none=True).tag(sync=True)
    unit = Unicode().tag(sync=True)
    was_selected = Int(allow_none=True).tag(sync=True)

    _deselected_color = "#D3D3D3"

    # Note: we pass in the data, rather than the layer itself,
    # to deal with cases where, for either setup or story reasons,
    # the layer doesn't exist in the viewer when we have to create
    # this component (which will be in the stage initializer)
    def __init__(self, viewers, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewers = viewers
        self.glue_data = data
        self._bins = kwargs.get("bins", None)
        self._original_colors = []
        if "options" in kwargs:
            self.options = kwargs["options"]
        self.subset_labels = kwargs.get("subset_labels", [])
        self.subset_group = kwargs.get("subset_group", False)
        self.lower_transform = kwargs.get("lower_transform", None)
        self.upper_transform = kwargs.get("upper_transform", None)
        self.subsets = []
        if "units" in kwargs:
            self.units = kwargs["units"]

    @property
    def bins(self):
        if self._bins is not None:
            return self._bins
        return [getattr(viewer.state, "bins", None) for viewer in self.viewers]

    def _update_subsets(self, states):
        if not self.subsets:
            kwargs = { "alpha": 1 }
            session = self.viewers[0].session
            for index in range(len(self.viewers)):
                data = self.glue_data[index]
                state = states[index]
                if self.subset_labels:
                    kwargs["label"] = self.subset_labels[index]
                kwargs["color"] = self._original_colors[index]
                if self.subset_group:
                    subset = session.data_collection.new_subset_group(state, **kwargs)
                else:
                    subset = data.new_subset(state, **kwargs)
                    self.viewers[index].add_subset(subset)
                self.subsets.append(subset)
        else:
            for (subset, state) in zip(self.subsets, states):
                subset.subset_state = state

    @property
    def layers(self):
        return [viewer.layer_artist_for_data(data) for (data, viewer) in zip(self.glue_data, self.viewers)]

    @observe('selected')
    def _update(self, change):
        if change["old"] is None:
            self._original_colors = [layer.state.color for layer in self.layers]

        selected = change["new"]
        if selected is None:
            states = []
            for index in range(len(self.viewers)):
                if self.layers[index] is not None:
                    self.layers[index].state.color = self._original_colors[index]
                state = array([False for _ in range(self.glue_data[index].size)])
                states.append(state)
            self._update_subsets(states)
            return

        around_median = selected / 2
        bottom_percent = 50 - around_median
        top_percent = 50 + around_median

        states = []
        for (index, viewer) in enumerate(self.viewers):
            component_id = viewer.state.x_att
            data = self.glue_data[index][component_id]
            self.layers[index].state.color = self._deselected_color
            bottom = percentile(data, bottom_percent, method="nearest")
            top = percentile(data, top_percent, method="nearest")
            state = RangeSubsetState(bottom, top, component_id)
            states.append(state)
            bins = self.bins[index]
            if bins is not None:
                bottom = next((x for x in bins if x > bottom), bottom)
                top = next((x for x in bins if x > top), top)
            if self.lower_transform is not None:
                bottom = self.lower_transform(bottom)
            if self.upper_transform is not None:
                top = self.upper_transform(top)

        self._update_subsets(states)

