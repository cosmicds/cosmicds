from ipyvuetify import VuetifyTemplate
from numpy import array, percentile
from traitlets import Int, List, Unicode, observe

from glue.core.subset import RangeSubsetState

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
        self.subset_labels = kwargs.get("subset_labels", [])
        self.subset_group = kwargs.get("subset_group", False)
        self.subsets = []
        if "units" in kwargs:
            self.units = kwargs["units"]

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
        for (index, viewer) in enumerate(self.viewers):
            component_id = viewer.state.x_att
            data = self.glue_data[index][component_id]
            layer = self.layers[index]
            layer.state.color = self._deselected_color
            bottom = percentile(data, bottom_percent, method="nearest")
            top = percentile(data, top_percent, method="nearest")
            state = RangeSubsetState(bottom, top, component_id)
            states.append(state)
            if self.resolution is not None:
                bottom = round(bottom, self.resolution)
                top = round(top, self.resolution)

            bottom_str = "{:g}".format(bottom)
            top_str = "{:g}".format(top)
            if self.units and self.units[index]:
                unit_str = f" {self.units[index]}"
            else:
                unit_str = ""
            label_text = f"{selected}%: {bottom_str} - {top_str}{unit_str}"
            viewer.figure.title = label_text
            viewer.figure.title_style = {
                "font-size": '1rem',
                "fill": "black"  # Since this is all happening in svg-land, use fill to set the text color
            }

        self._update_subsets(states)

