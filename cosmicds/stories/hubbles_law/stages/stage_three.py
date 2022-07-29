from os.path import join
from pathlib import Path
from functools import partial

from echo import CallbackProperty

from glue.core.message import NumericalDataChangedMessage
from traitlets import default, Bool

from cosmicds.components.table import Table
from cosmicds.phases import CDSState
from cosmicds.registries import register_stage
from cosmicds.stories.hubbles_law.data_management import ALL_CLASS_SUMMARIES_LABEL, ALL_DATA_LABEL, ALL_STUDENT_SUMMARIES_LABEL, CLASS_DATA_LABEL, CLASS_SUMMARY_LABEL, STUDENT_DATA_LABEL
from cosmicds.stories.hubbles_law.stage import HubbleStage
from cosmicds.components.generic_state_component import GenericStateComponent
from cosmicds.stories.hubbles_law.viewers.viewers import HubbleClassHistogramView, HubbleHistogramView
from cosmicds.utils import extend_tool, load_template

from cosmicds.stories.hubbles_law.histogram_listener import HistogramListener
from cosmicds.stories.hubbles_law.viewers import HubbleFitView, HubbleScatterView

class StageState(CDSState):
    marker = CallbackProperty("")
    indices = CallbackProperty({})
    advance_marker = CallbackProperty(True)

    markers = CallbackProperty([
        'ran_mar1',
        'ran_mar2',
        'ran_mar3',
        'ran_mar4',
        'ran_mar5',
        'ran_mar6',
        'ran_mar7',
        'ran_mar8',
        'ran_mar9',
        'ran_mar10',
        'ran_mar11',
        'ran_mar12',
    ])

    step_markers = CallbackProperty([
    ])

    table_show = CallbackProperty([
        'ran_mar1',
        'ran_mar2',
        'ran_mar3',
    ])

    table_highlights = CallbackProperty([
    ])

    all_galaxies_morph_plot_show = CallbackProperty([
    ])

    all_galaxies_morph_plot_highlights = CallbackProperty([
    ])

    my_galaxies_plot_show = CallbackProperty([
        'ran_mar2',
        'ran_mar3',
    ])

    my_galaxies_plot_highlights = CallbackProperty([
    ])

    all_galaxies_plot_show = CallbackProperty([
    ])

    all_galaxies_plot_highlights = CallbackProperty([
    ])

    my_class_hist_show = CallbackProperty([
    ])

    my_class_hist_highlights = CallbackProperty([
    ])

    all_classes_hist_show = CallbackProperty([
    ])

    all_classes_hist_highlights = CallbackProperty([
    ])

    sandbox_hist_show = CallbackProperty([
    ])

    sandbox_hist_highlights = CallbackProperty([
    ])


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.marker_index = 0
        self.marker = self.markers[0]
        self.indices = {marker: idx for idx, marker in enumerate(self.markers)}

    def marker_before(self, marker):
        return self.indices[self.marker] < self.indices[marker]

    def move_marker_forward(self, marker_text, _value=None):
        index = min(self.markers.index(marker_text) + 1, len(self.markers) - 1)
        self.marker = self.markers[index]


@register_stage(story="hubbles_law", index=4, steps=[
    "MY DATA",
    "CLASS DATA",
    "BY GALAXY TYPE",
    "PROFESSIONAL DATA"
])
class StageThree(HubbleStage):
    show_team_interface = Bool(False).tag(sync=True)

    @default('stage_state')
    def _default_state(self):
        return StageState()

    @default('template')
    def _default_template(self):
        return load_template("stage_three.vue", __file__)

    @default('stage_icon')
    def _default_stage_icon(self):
        return "3"
    
    @default('title')
    def _default_title(self):
        return "Explore Data"

    @default('subtitle')
    def _default_subtitle(self):
        return "Perhaps a small blurb about this stage"

    viewer_ids_for_data = {
        STUDENT_DATA_LABEL : ["fit_viewer", "comparison_viewer"],
        CLASS_DATA_LABEL: ["comparison_viewer"],
        CLASS_SUMMARY_LABEL: ["class_distr_viewer"]
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stage_state = StageState()
        self.show_team_interface = self.app_state.show_team_interface

        student_data = self.get_data(STUDENT_DATA_LABEL)
        all_data = self.get_data(ALL_DATA_LABEL)
        class_meas_data = self.get_data(CLASS_DATA_LABEL)

        fit_table = Table(self.session,
                    data=student_data,
                    glue_components=['name',
                                    'type',
                                    'velocity',
                                    'distance'],
                    key_component='name',
                    names=['Galaxy Name',
                        'Galaxy Type',
                        'Velocity (km/s)',
                        'Distance (Mpc)'],
                    title='My Galaxies',
                    subset_label="fit_table_selected"
        )
        self.add_widget(fit_table, label="fit_table")

        # Set up links between various data sets
        hubble_dc_name = "Hubble 1929-Table 1"
        hstkp_dc_name = "HSTkey2001"
        galaxy_dc_name = "galaxy_data"

        dist_attr = "distance"
        vel_attr = "velocity"
        for field in [dist_attr, vel_attr]:
            self.add_link(CLASS_DATA_LABEL, field, ALL_DATA_LABEL, field)
        self.add_link(hubble_dc_name, 'Distance (Mpc)', hstkp_dc_name, 'Distance (Mpc)')
        self.add_link(hubble_dc_name, 'Tweaked Velocity (km/s)', hstkp_dc_name, 'Velocity (km/s)')
        self.add_link(hstkp_dc_name, 'Distance (Mpc)', STUDENT_DATA_LABEL, 'distance')
        self.add_link(hstkp_dc_name, 'Velocity (km/s)', STUDENT_DATA_LABEL, 'velocity')


        # Create viewers
        fit_viewer = self.add_viewer(HubbleFitView, "fit_viewer", "My Data")
        comparison_viewer = self.add_viewer(HubbleScatterView, "comparison_viewer", "Data Comparison")
        morphology_viewer = self.add_viewer(HubbleScatterView, "morphology_viewer", "Galaxy Morphology")
        prodata_viewer = self.add_viewer(HubbleScatterView, "prodata_viewer", "Professional Data")
        class_distr_viewer = self.add_viewer(HubbleClassHistogramView, 'class_distr_viewer', "My Class")
        all_distr_viewer = self.add_viewer(HubbleHistogramView, 'all_distr_viewer', "All Classes")
        sandbox_distr_viewer = self.add_viewer(HubbleHistogramView, 'sandbox_distr_viewer', "Sandbox")


        # Set up the generic state components
        state_components_dir = str(
            Path(__file__).parent.parent / "components" / "generic_state_components" / "stage_three")
        path = join(state_components_dir, "")
        state_components = [
            "guideline_intro_explore",
            "guideline_observe_trends_mc",
            "guideline_trend_lines_draw",
        ]
        ext = ".vue"
        for comp in state_components:
            label = f"c-{comp}".replace("_", "-")

            # comp + ext = filename; path = folder where they live.
            component = GenericStateComponent(comp + ext, path, self.stage_state)
            self.add_component(component, label=label)


        # Grab data
        class_sample_data = self.get_data(CLASS_SUMMARY_LABEL)
        students_summary_data = self.get_data(ALL_STUDENT_SUMMARIES_LABEL)
        classes_summary_data = self.get_data(ALL_CLASS_SUMMARIES_LABEL)
        hubble1929 = self.get_data(hubble_dc_name)
        hstkp = self.get_data(hstkp_dc_name)
        galaxy_data = self.get_data(galaxy_dc_name)

        # Set up the listener to sync the histogram <--> scatter viewers

        # Set up the functionality for the histogram <---> scatter sync
        # We add a listener for when a subset is modified/created on 
        # the histogram viewer as well as extend the xrange tool for the 
        # histogram to always affect this subset
        histogram_source_label = "histogram_source_subset"
        histogram_modify_label = "histogram_modify_subset"
        self.histogram_listener = HistogramListener(self.story_state,
                                                    None,
                                                    class_sample_data,
                                                    None, 
                                                    class_meas_data,
                                                    source_subset_label=histogram_source_label,
                                                    modify_subset_label=histogram_modify_label)

        not_ignore = {
            fit_table.subset_label: [fit_viewer],
            histogram_source_label: [class_distr_viewer],
            histogram_modify_label: [comparison_viewer]
        }
        def label_ignore(x, label):
            return x.label == label
        for label, listeners in not_ignore.items():
            ignorer = partial(label_ignore, label=label)
            for viewer in self.all_viewers:
                if viewer not in listeners:
                    viewer.ignore(ignorer)

        def comparison_ignorer(x):
            return x.label == histogram_modify_label and x.data != self.histogram_listener.modify_data
        comparison_viewer.ignore(comparison_ignorer)

        for viewer in [fit_viewer, comparison_viewer, prodata_viewer]:
            viewer.add_data(student_data)
            #viewer.layers[-1].state.visible = False
            viewer.state.x_att = student_data.id[dist_attr]
            viewer.state.y_att = student_data.id[vel_attr]
        
        student_layer = comparison_viewer.layers[-1]
        student_layer.state.color = 'green'
        student_layer.state.zorder = 3
        student_layer.state.size = 8
        comparison_viewer.add_data(class_meas_data)
        class_layer = comparison_viewer.layers[-1]
        class_layer.state.zorder = 2
        class_layer.state.color = 'red'
        # comparison_viewer.add_data(all_data)
        # all_layer = comparison_viewer.layers[-1]
        # all_layer.state.zorder = 1
        # all_layer.state.visible = False
        comparison_viewer.state.x_att = student_data.id[dist_attr]
        comparison_viewer.state.y_att = student_data.id[vel_attr]
        comparison_viewer.state.reset_limits()
        
        prodata_viewer.add_data(student_data)
        prodata_viewer.state.x_att = student_data.id[dist_attr]
        prodata_viewer.state.y_att = student_data.id[vel_attr]
        prodata_viewer.add_data(hstkp)
        prodata_viewer.add_data(hubble1929)

        histogram_viewers = [class_distr_viewer, all_distr_viewer, sandbox_distr_viewer]
        for viewer in histogram_viewers:
            label = 'Count' if viewer == class_distr_viewer else 'Proportion'
            viewer.figure.axes[1].label = label
            if viewer != all_distr_viewer:
                viewer.add_data(class_sample_data)
                layer = viewer.layers[-1]
                layer.state.color = 'red'
                layer.state.alpha = 0.5
            if viewer != class_distr_viewer:
                viewer.add_data(students_summary_data)
                layer = viewer.layers[-1]
                layer.state.color = 'blue'
                layer.state.alpha = 0.5
                viewer.add_data(classes_summary_data)
                layer = viewer.layers[-1]
                layer.state.color = '#f0c470'
                layer.state.alpha = 0.5
                viewer.state.normalize = True
                viewer.state.y_min = 0
                viewer.state.y_max = 1
                viewer.state.hist_n_bin = 30
    
        class_distr_viewer.state.x_att = class_sample_data.id['age']
        all_distr_viewer.state.x_att = students_summary_data.id['age']
        sandbox_distr_viewer.state.x_att = students_summary_data.id['age']

        # Do some stuff with the galaxy data
        type_field = 'type'
        elliptical_subset = all_data.new_subset(all_data.id[type_field] == 'E', label='Elliptical', color='orange')
        spiral_subset = all_data.new_subset(all_data.id[type_field] == 'Sp', label='Spiral', color='green')
        irregular_subset = all_data.new_subset(all_data.id[type_field] == 'Ir', label='Irregular', color='red')
        morphology_subsets = [elliptical_subset, spiral_subset, irregular_subset]
        for subset in morphology_subsets:
            morphology_viewer.add_subset(subset)
        morphology_viewer.state.x_att = all_data.id['distance']
        morphology_viewer.state.y_att = all_data.id['velocity']

        # Just for accessibility while testing
        self.data_collection.histogram_listener = self.histogram_listener

        # Whenever data is updated, the appropriate viewers should update their bounds
        self.hub.subscribe(self, NumericalDataChangedMessage,
                           handler=self._on_data_change)

        def hist_selection_activate():
            if self.histogram_listener.source_subset is None:
                self.histogram_listener.source_subset = self.data_collection.new_subset_group(label=self.histogram_listener.source_subset_label)
            self.session.edit_subset_mode.edit_subset = [self.histogram_listener.source_subset]
        def hist_selection_deactivate():
            self.session.edit_subset_mode.edit_subset = []
        extend_tool(class_distr_viewer, 'bqplot:xrange', hist_selection_activate, hist_selection_deactivate)

        # We want the hub_fit_viewer to be selecting for the same subset as the table
        def fit_selection_activate():
            table = self.get_widget('fit_table')
            table.initialize_subset_if_needed()
            self.session.edit_subset_mode.edit_subset = [table.subset]
        def fit_selection_deactivate():
            self.session.edit_subset_mode.edit_subset = []
        extend_tool(fit_viewer, 'bqplot:rectangle', fit_selection_activate, fit_selection_deactivate)

    @property
    def all_viewers(self):
        return [layout.viewer for layout in self.viewers.values()]

    def _on_data_change(self, msg):
        viewer_id = self.viewer_ids_for_data.get(msg.data.label, [])
        for vid in viewer_id:
            self.get_viewer(vid).state.reset_limits()

    def table_selected_color(self, dark):
        return "colors.lightBlue.darken4"
