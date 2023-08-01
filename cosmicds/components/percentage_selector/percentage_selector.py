from ipyvuetify import VuetifyTemplate
from numpy import argsort, array
from traitlets import Int, List, Unicode, observe

from glue.core.subset import ElementSubsetState

from ...utils import load_template, percent_around_center_indices

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

    def _rounded_bound(self, bound):
        if self.resolution is None:
            return bound
        return round(bound, self.resolution)

    def _bin_rounded_bound(self, bound, bins):
        rounded_bound = self._rounded_bound(bound)
        resolution = 10 ** (-self.resolution)
        rounded_bin_bounds = self._bin_bounds(bound, bins)
        if bound < rounded_bin_bounds[0]:
            rounded_bound -= resolution
        elif bound > rounded_bin_bounds[1]:
            rounded_bound += resolution
        return rounded_bound

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

        states = []
        for index, (viewer, bins) in enumerate(zip(self.viewers, self.bins)):
            component_id = viewer.state.x_att
            data = self.glue_data[index][component_id]
            layer = self.layers[index]
            layer.state.color = self._deselected_color
            bottom_index, top_index = percent_around_center_indices(data.size, selected)
    
            sorted_indices = argsort(data)
            true_bottom = data[sorted_indices[bottom_index]]
            true_top = data[sorted_indices[top_index]]
            expected_count = round(selected * data.size / 100)
            actual_count = top_index - bottom_index + 1
            if expected_count != actual_count:
                median = self.glue_data[index].compute_statistic('median', viewer.state.x_att)
                if expected_count < actual_count:
                    dist_bottom = abs(median - true_bottom)
                    dist_top = abs(median - true_top)
                    new_bottom_index = bottom_index + 1
                    new_top_index = top_index - 1

                    if dist_bottom > dist_top:
                        bottom_index = new_bottom_index
                        true_bottom = data[sorted_indices[bottom_index]]
                    else:
                        top_index = new_top_index
                        true_top = data[sorted_indices[top_index]]
                else:
                    new_bottom_index = max(0, bottom_index - 1)
                    new_bottom = data[sorted_indices[new_bottom_index]]
                    new_top_index = min(top_index + 1, data.size - 1)
                    new_bottom = data[sorted_indices[new_top_index]]
                    dist_bottom = abs(median - new_bottom)
                    dist_top = abs(median - new_bottom)

                    if dist_bottom < dist_top or new_top_index == data.size - 1:
                        bottom_index = new_bottom_index
                        true_bottom = data[sorted_indices[bottom_index]]
                    else:
                        top_index = new_top_index
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
            rounded_bottom = self._bin_rounded_bound(true_bottom, bins)
            rounded_top = self._bin_rounded_bound(true_top, bins)

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
                "transform": "translate(-25%, 5px)"
            }

        self._update_subsets(states)

