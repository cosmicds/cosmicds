import solara


@solara.component
def PercentageSelector(viewers, glue_data, bins=None, **kwargs):
    
    radio_color = "#1e90ff"
    options = [50, 68, 95]
    selected = None
    resolution = kwargs.get("resolution", None)
    subset_group = kwargs.get("subset_group", False)
    subset_labels = kwargs.get("subset_labels", [])
    bins = bins or [getattr(viewer.state, "bins", None) for viewer in viewers]
    subsets = []

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
