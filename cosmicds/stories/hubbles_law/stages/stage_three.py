from functools import partial
from glue.core.message import NumericalDataChangedMessage
from glue.core.state_objects import State
from glue.core.subset_group import SubsetGroup
from traitlets import default

from cosmicds.components.table import Table
from cosmicds.registries import register_stage
from cosmicds.stories.hubbles_law.stage import HubbleStage
from cosmicds.stories.hubbles_law.viewers.viewers import HubbleClassHistogramView, HubbleHistogramView
from cosmicds.utils import extend_tool, load_template
from cosmicds.viewers import CDSHistogramView

from cosmicds.stories.hubbles_law.histogram_listener import HistogramListener
from cosmicds.stories.hubbles_law.viewers import HubbleFitView, HubbleScatterView

class StageState(State):
    pass

@register_stage(story="hubbles_law", index=3, steps=[
    "My data",
    "Class data",
    "Galaxy Type",
    "Professional Science Data"
])
class StageThree(HubbleStage):
    @default('stage_state')
    def _default_state(self):
        return StageState()

    @default('template')
    def _default_template(self):
        return load_template("stage_three.vue", __file__)
    
    @default('title')
    def _default_title(self):
        return "Explore Data"

    @default('subtitle')
    def _default_subtitle(self):
        return "Perhaps a small blurb about this stage"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        measurements = self.get_data("student_measurements")
        fit_table = Table(self.session,
                    data=measurements,
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
        student_dc_name = "student_data"
        class_dc_name = "class_data"
        all_dc_name = "HubbleData_All"
        hubble_dc_name = "Hubble 1929-Table 1"
        hstkp_dc_name = "HSTkey2001"
        galaxy_dc_name = "galaxy_data"
        

        student_data = self.get_data(student_dc_name)
        all_data = self.get_data(all_dc_name)
        class_meas_data = self.get_data(class_dc_name)
        print(all_data)

        dist_attr = "distance"
        vel_attr = "velocity"
        for field in [dist_attr, vel_attr]:
            self.add_link(class_dc_name, field, all_dc_name, field)
        self.add_link(hubble_dc_name, 'Distance (Mpc)', hstkp_dc_name, 'Distance (Mpc)')
        self.add_link(hubble_dc_name, 'Tweaked Velocity (km/s)', hstkp_dc_name, 'Velocity (km/s)')
        self.add_link(hstkp_dc_name, 'Distance (Mpc)', student_dc_name, 'distance')
        self.add_link(hstkp_dc_name, 'Velocity (km/s)', student_dc_name, 'velocity')


        # Create viewers
        fit_viewer = self.add_viewer(HubbleFitView, "fit_viewer", "My Data")
        comparison_viewer = self.add_viewer(HubbleScatterView, "comparison_viewer", "Data Comparison")
        morphology_viewer = self.add_viewer(HubbleScatterView, "morphology_viewer", "Galaxy Morphology")
        prodata_viewer = self.add_viewer(HubbleScatterView, "prodata_viewer", "Professional Data")
        class_distr_viewer = self.add_viewer(HubbleClassHistogramView, 'class_distr_viewer', "My Class")
        all_distr_viewer = self.add_viewer(HubbleHistogramView, 'all_distr_viewer', "All Classes")
        sandbox_distr_viewer = self.add_viewer(HubbleHistogramView, 'sandbox_distr_viewer', "Sandbox")

        # Grab data
        class_sample_data = self.get_data("HubbleSummary_ClassSample")
        students_summary_data = self.get_data("HubbleSummary_Students")
        classes_summary_data = self.get_data("HubbleSummary_Classes")
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
        comparison_viewer.add_data(class_meas_data)
        class_layer = comparison_viewer.layers[-1]
        class_layer.state.zorder = 2
        class_layer.state.color = 'red'
        comparison_viewer.add_data(all_data)
        all_layer = comparison_viewer.layers[-1]
        all_layer.state.zorder = 1
        all_layer.state.visible = False
        comparison_viewer.state.x_att = all_data.id[dist_attr]
        comparison_viewer.state.y_att = all_data.id[vel_attr]
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
        type_field = 'MorphType'
        elliptical_subset = galaxy_data.new_subset(galaxy_data.id[type_field] == 'E', label='Elliptical', color='orange')
        spiral_subset = galaxy_data.new_subset(galaxy_data.id[type_field] == 'Sp', label='Spiral', color='green')
        irregular_subset = galaxy_data.new_subset(galaxy_data.id[type_field] == 'Ir', label='Irregular', color='red')
        morphology_subsets = [elliptical_subset, spiral_subset, irregular_subset]
        for subset in morphology_subsets:
            morphology_viewer.add_subset(subset)
        morphology_viewer.state.x_att = galaxy_data.id['EstDist_Mpc']
        morphology_viewer.state.y_att = galaxy_data.id['velocity_km_s']

        # Just for accessibility while testing
        self.data_collection.histogram_listener = self.histogram_listener

        # Whenever the student data is updated, the student scatter viewer should update its bounds
        self.hub.subscribe(self, NumericalDataChangedMessage,
                           handler=self._on_student_data_change, filter=self._student_data_filter)

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

    def _student_data_filter(self, msg):
        return msg.data == self.get_data("student_data")

    def _on_student_data_change(self, msg):
        viewer = self.get_viewer("fit_viewer")
        viewer.state.reset_limits()

    def table_selected_color(self, dark):
        return "colors.lightBlue.darken4"
