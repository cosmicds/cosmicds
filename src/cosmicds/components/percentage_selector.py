from numpy import argsort, array
import solara
import reacton.ipyvuetify as rv

from glue.core.subset import ElementSubsetState

from ..utils import percent_around_center_indices


@solara.component
def PercentageSelector(viewers, glue_data, bins=None, **kwargs):
    
    radio_color = "#1e90ff"
    options = [50, 68, 95]
    selected = solara.use_reactive(None)
    last_updated = None
    resolution = kwargs.get("resolution", 0)
    subset_group = kwargs.get("subset_group", False)
    subset_labels = kwargs.get("subset_labels", [])
    bins = bins or [getattr(viewer.state, "bins", None) for viewer in viewers]
    subsets = []
    original_colors = []
    units = kwargs.get("units", [])

    deselected_color = "#a9a9a9"

    def _update_subsets(states):
        if not subsets:
            kwargs = { "alpha": 1 }
            session = viewers[0].session
            for index in range(len(viewers)):
                data = glue_data[index]
                state = states[index]
                if subset_labels:
                    kwargs["label"] = subset_labels[index]
                if subset_group:
                    subset = session.data_collection.new_subset_group(state, **kwargs)
                else:
                    subset = data.new_subset(state, **kwargs)
                    viewers[index].add_subset(subset)
                subsets.append(subset)
        else:
            for subset, state in zip(subsets, states):
                subset.subset_state = state

    def _bin_bounds(value, bins):
        index = next((idx for idx, x in enumerate(bins) if x >= value), 0)
        return bins[index - 1], bins[index]

    def _rounded_bound(bound):
        if resolution is None:
            return bound
        return round(bound, resolution)

    def _bin_rounded_bound(bound, bins):
        rounded_bound = _rounded_bound(bound)
        res = 10 ** (-resolution)
        rounded_bin_bounds = _bin_bounds(bound, bins)
        if bound < rounded_bin_bounds[0]:
            rounded_bound -= res 
        elif bound > rounded_bin_bounds[1]:
            rounded_bound += res 
        return rounded_bound

    def _update():
        nonlocal original_colors, last_updated

        option = selected.value
        if last_updated == option:
            return option

        layers = [viewer.layer_artist_for_data(data)
                  for (data, viewer) in zip(glue_data, viewers)]
        if last_updated is None:
            original_colors = [layer.state.color for layer in layers]

        if option is None:
            states = []
            for (index, viewer) in enumerate(viewers):
                if layers[index] is not None:
                    layers[index].state.color = original_colors[index]
                    # viewer_layouts[index].set_subtitle(None)
                state = array([False for _ in range(glue_data[index].size)])
                states.append(state)
            _update_subsets(states)
            return option

        states = []
        for index, (viewer, viewer_bins) in enumerate(zip(viewers, bins)):
            component_id = viewer.state.x_att
            data = glue_data[index][component_id]
            layer = layers[index]
            layer.state.color = deselected_color
            bottom_index, top_index = percent_around_center_indices(data.size, option)
    
            sorted_indices = argsort(data)
            true_bottom = data[sorted_indices[bottom_index]]
            true_top = data[sorted_indices[top_index]]
            expected_count = round(option * data.size / 100)
            actual_count = top_index - bottom_index + 1
            if expected_count != actual_count:
                median = glue_data[index].compute_statistic('median', viewer.state.x_att)
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
            rounded_bottom = _bin_rounded_bound(true_bottom, viewer_bins)
            rounded_top = _bin_rounded_bound(true_top, viewer_bins)

            bottom_str = "{:g}".format(rounded_bottom)
            top_str = "{:g}".format(rounded_top)
            if units and units[index]:
                unit_str = f" {units[index]}"
            else:
                unit_str = ""
            label_text = f"{option}% range: {bottom_str} \u2013 {top_str}{unit_str}"
            # self.viewer_layouts[index].set_subtitle(label_text)

        _update_subsets(states)

        return option

    def _update_selected(option, value):
        nonlocal last_updated
        if value:
            selected.set(option)
        elif selected.value == option:
            selected.set(None)
        last_updated = _update()

    def _model_factory(option):
        return solara.lab.computed(lambda option=option: selected.value == option)

    with rv.Card():
        with rv.Container():
            for option in options:
                model = _model_factory(option)
                solara.Switch(value=model,
                              label=f"{option}%",
                              on_value=lambda value, option=option: _update_selected(option, value))
