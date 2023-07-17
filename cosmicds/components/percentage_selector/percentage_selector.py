from math import ceil, floor

from ipyvuetify import VuetifyTemplate
from numpy import argsort, array
from traitlets import Int, List, Unicode, observe

from glue.core.subset import ElementSubsetState

from ...utils import load_template

class PercentageSelector(VuetifyTemplate):
    
    template = load_template("percentage_selector.vue", __file__, traitlet=True).tag(sync=True)
    radio_color = Unicode("#1e90ff").tag(sync=True)
    options = List([50, 68, 95]).tag(sync=True)
    selected = Int(None, allow_none=True).tag(sync=True)
    unit = Unicode().tag(sync=True)
    was_selected = Int(allow_none=True).tag(sync=True)

    _deselected_color = "#a9a9a9"

    # Note: we pass in the data, rather than the layer itself,
    # to deal with cases where, for either setup or story reasons,
    # the layer doesn't exist in the viewer when we have to create
    # this component (which will be in the stage initializer)
    def __init__(self, viewers, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewers = viewers
        self.glue_data = data
        self._original_colors = []
        self.resolution = kwargs.get("resolution", None)  # Number of decimal places for reporting bounds
        if "options" in kwargs:
            self.options = kwargs["options"]
        self._bins = kwargs.get("bins", None)
        self.subset_labels = kwargs.get("subset_labels", [])
        self.subset_group = kwargs.get("subset_group", False)
        self.subsets = []
        if "units" in kwargs:
            self.units = kwargs["units"]
            
    @property
    def bins(self):
        if self._bins is not None:
            return self._bins
        return [getattr(viewer.state, "bins", None) for viewer in self.viewers]

    def percentile_index(self, size, percent, method=round):
        return min(method(size * percent / 100), size - 1)

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

    @staticmethod
    def _bin_bounds(value, bins):
        index = next((idx for idx, x in enumerate(bins) if x >= value), 0)
        return bins[index - 1], bins[index]

    @observe('selected')
    def _update(self, change):
        if change["old"] is None:
            self._original_colors = [layer.state.color for layer in self.layers]

        selected = change["new"]
        if selected is None:
            states = []
            for (index, viewer) in enumerate(self.viewers):
                if self.layers[index] is not None:
                    self.layers[index].state.color = self._original_colors[index]
                    viewer.figure.title = ""
                    viewer.figure.title_style = {}
                state = array([False for _ in range(self.glue_data[index].size)])
                states.append(state)
            self._update_subsets(states)
            return

        around_median = selected / 2
        bottom_percent = 50 - around_median
        top_percent = 50 + around_median

        states = []
        for index, (viewer, bins) in enumerate(zip(self.viewers, self.bins)):
            component_id = viewer.state.x_att
            data = self.glue_data[index][component_id]
            layer = self.layers[index]
            layer.state.color = self._deselected_color
            bottom_index = self.percentile_index(data.size, bottom_percent, method=ceil)
            top_index = self.percentile_index(data.size, top_percent, method=floor)
            sorted_indices = argsort(data)
            true_bottom = data[sorted_indices[bottom_index]]
            true_top = data[sorted_indices[top_index]]

            # Ideally we could use something like a RangeSubsetState
            # but this can be problematic for our case when there are a small number
            # of data points and low resolution, since then repeated values will
            # have a very noticeable bad effect on the size that we're choosing
            # If in the future we have a situation where we want to do this with more fluid
            # data, we'll need to list to an update message or something to recalculate the
            # indices here
            indices = [si for i, si in enumerate(sorted_indices) if i >= bottom_index and i <= top_index]
            state = ElementSubsetState(indices=indices)
            states.append(state)
            if self.resolution is not None:
                rounded_bottom = round(true_bottom, self.resolution)
                rounded_top = round(true_top, self.resolution)
            else:
                rounded_bottom = true_bottom
                rounded_top = true_top

            if bins is not None:
                resolution = 10 ** (-self.resolution)
                bins_rounded_bottom = self._bin_bounds(rounded_bottom, bins)
                if true_bottom < bins_rounded_bottom[0]:
                    rounded_bottom -= resolution
                elif true_bottom > bins_rounded_bottom[1]:
                    rounded_bottom += resolution 

                bins_rounded_top = self._bin_bounds(rounded_top, bins)
                if true_top < bins_rounded_top[0]:
                    rounded_top -= resolution
                elif true_top > bins_rounded_top[1]:
                    rounded_top += resolution

            bottom_str = "{:g}".format(rounded_bottom)
            top_str = "{:g}".format(rounded_top)
            if self.units and self.units[index]:
                unit_str = f" {self.units[index]}"
            else:
                unit_str = ""
            label_text = f"{selected}%: {bottom_str} - {top_str}{unit_str}"
            viewer.figure.title = label_text
            viewer.figure.title_style = {
                "font-size": '1rem',
                "fill": "black",  # Since this is all happening in svg-land, use fill to set the text color
                "transform": "translate(0, 5px)"
            }

        self._update_subsets(states)

