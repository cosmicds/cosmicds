from glue.core import Data
from glue.core.state_objects import State
from traitlets import default

from cosmicds.components.table import Table
from cosmicds.registries import register_stage
from cosmicds.phases import Stage
from cosmicds.utils import extend_tool, load_template, update_figure_css
from cosmicds.viewers import CDSHistogramView, CDSScatterView

from cosmicds.stories.hubbles_law.histogram_listener import HistogramListener
from cosmicds.stories.hubbles_law.viewers import CDSFitView

class StageState(State):
    pass

@register_stage(story="hubbles_law", index=3, steps=[
    "My data",
    "Class data",
    "Galaxy Type",
    "Professional Science Data"
])
class StageThree(Stage):
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

        # measurements = self.get_data("student_measurements")
        # fit_table = Table(self.session,
        #                   data=measurements,
        #                   glue_components=['ID',
        #                                   'Type',
        #                                   'velocity',
        #                                   'distance'],
        #                   key_component='ID',
        #                   names=['Galaxy Name',
        #                       'Galaxy Type',
        #                       'Velocity (km/s)',
        #                       'Distance (Mpc)'],
        #                   title='My Galaxies')
        # self.add_widget(fit_table, label="fit_table")

        # student_data = self.get_data("student_data")
        # all_data = self.get_data("HubbleData_All")


        # # Set up links between various data sets
        # student_dc_name = "student_data"
        # class_dc_name = "HubbleData_ClassSample"
        # all_dc_name = "HubbleData_All"
        # hubble_name = "Hubble 1929-Table 1"
        # hstkp_name = "HSTkey2001"

        # class_data = self.get_data(class_dc_name)
        # for component in class_data.components:
        #     field = component.label
        #     self.add_link(class_dc_name, field, all_dc_name, field)
        #     if component.label in student_data.component_ids():
        #         self.add_link(student_dc_name, field, class_dc_name, field)
        # self.add_link(hubble_name, 'Distance (Mpc)', hstkp_name, 'Distance (Mpc)')
        # self.add_link(hubble_name, 'Tweaked Velocity (km/s)', hstkp_name, 'Velocity (km/s)')
        # self.add_link(hstkp_name, 'Distance (Mpc)', student_dc_name, 'distance')
        # self.add_link(hstkp_name, 'Velocity (km/s)', student_dc_name, 'velocity')


        # students_viewer = self.add_viewer(CDSScatterView, "students_viewer", "Student Data")
        # fit_viewer = self.add_viewer(CDSFitView, "fit_viewer", "My Data")
        # comparison_viewer = self.add_viewer(CDSScatterView, "comparison_viewer", "Data Comparison")
        # morphology_viewer = self.add_viewer(CDSScatterView, "morphology_viewer", "Galaxy Morphology")
        # prodata_viewer = self.add_viewer(CDSScatterView, "prodata_viewer", "Professional Data")
        # for viewer in [students_viewer, fit_viewer, comparison_viewer, prodata_viewer]:
        #     viewer.add_data(student_data)
        #     #viewer.layers[-1].state.visible = False
        #     viewer.state.x_att = student_data.id['distance']
        #     viewer.state.y_att = student_data.id['velocity']


        # students_viewer.add_data(class_data)
        # students_viewer.state.x_att = class_data.id['distance']
        # students_viewer.state.y_att = class_data.id['velocity']
        # students_viewer.layers[-1].state.zorder = 2
        
        # comparison_viewer.layers[-1].state.zorder = 3
        # comparison_viewer.add_data(class_data)
        # comparison_viewer.layers[-1].state.zorder = 2
        # comparison_viewer.add_data(all_data)
        # comparison_viewer.layers[-1].state.zorder = 1
        # comparison_viewer.state.x_att = all_data.id['distance']
        # comparison_viewer.state.y_att = all_data.id['velocity']
        # comparison_viewer.state.reset_limits()
        
        # hubble1929 = self.get_data("Hubble 1929-Table 1")
        # hstkp = self.get_data("HSTkey2001")
        # prodata_viewer.add_data(student_data)
        # prodata_viewer.state.x_att = student_data.id['distance']
        # prodata_viewer.state.y_att = student_data.id['velocity']
        # prodata_viewer.add_data(hstkp)
        # prodata_viewer.add_data(hubble1929)

        # class_distr_viewer = self.add_viewer(CDSHistogramView, 'class_distr_viewer')
        # all_distr_viewer = self.add_viewer(CDSHistogramView, 'all_distr_viewer')
        # sandbox_distr_viewer = self.add_viewer(CDSHistogramView, 'sandbox_distr_viewer')
        # class_sample_data = self.get_data("HubbleSummary_ClassSample")
        # students_summary_data = self.get_data("HubbleSummary_Students")
        # classes_summary_data = self.get_data("HubbleSummary_Classes")
        # histogram_viewers = [class_distr_viewer, all_distr_viewer, sandbox_distr_viewer]
        # for viewer in histogram_viewers:
        #     label = 'Count' if viewer == class_distr_viewer else 'Proportion'
        #     viewer.figure.axes[1].label = label
        #     if viewer != all_distr_viewer:
        #         viewer.add_data(class_sample_data)
        #         layer = viewer.layers[-1]
        #         layer.state.color = 'red'
        #         layer.state.alpha = 0.5
        #     if viewer != class_distr_viewer:
        #         viewer.add_data(students_summary_data)
        #         layer = viewer.layers[-1]
        #         layer.state.color = 'blue'
        #         layer.state.alpha = 0.5
        #         viewer.add_data(classes_summary_data)
        #         layer = viewer.layers[-1]
        #         layer.state.color = '#f0c470'
        #         layer.state.alpha = 0.5
        #         viewer.state.normalize = True
        #         viewer.state.y_min = 0
        #         viewer.state.y_max = 1
        #         viewer.state.hist_n_bin = 30
    
        # class_distr_viewer.state.x_att = class_sample_data.id['age']
        # all_distr_viewer.state.x_att = students_summary_data.id['age']
        # sandbox_distr_viewer.state.x_att = students_summary_data.id['age']

        # galaxy_data = self.get_data('galaxy_data')
        # type_field = 'MorphType'
        # elliptical_subset = galaxy_data.new_subset(galaxy_data.id[type_field] == 'E', label='Elliptical', color='orange')
        # spiral_subset = galaxy_data.new_subset(galaxy_data.id[type_field] == 'Sp', label='Spiral', color='green')
        # irregular_subset = galaxy_data.new_subset(galaxy_data.id[type_field] == 'Ir', label='Irregular', color='red')
        # morphology_subsets = [elliptical_subset, spiral_subset, irregular_subset]
        # for subset in morphology_subsets:
        #     morphology_viewer.add_subset(subset)
        # morphology_viewer.state.x_att = galaxy_data.id['EstDist_Mpc']
        # morphology_viewer.state.y_att = galaxy_data.id['velocity_km_s']

        # Set up the listener to sync the histogram <--> scatter viewers
    #    meas_data = self.get_data("HubbleData_ClassSample")
    #    hist_sync_sg = self.data_collection.new_subset_group(label="Hist Sync SG")
    #   scatter_sync_sg = self.data_collection.new_subset_group(label="Scatter Sync SG")
    #    hist_sync_sg.style.color = "green"
    #    scatter_sync_sg.style.color = "green"

        # Right now, this is the only viewer aside from the synced viewers
        # that shows these data objects
    #    for layer in sandbox_distr_viewer.layers:
    #        if layer.state.layer.label in [hist_sync_sg.label, scatter_sync_sg.label]:
    #            layer.state.visible = False

        # fit_table = self.get_widget("fit_table")
        # subset_group_label = "fit_table" + '_selected'
        # fit_table.subset_group = self.data_collection.new_subset_group(label=subset_group_label, subset_state=None)

        # # Set up the functionality for the histogram <---> scatter sync
        # # We add a listener for when a subset is modified/created on 
        # # the histogram viewer as well as extend the xrange tool for the 
        # # histogram to always affect this subset
        # self.histogram_listener = HistogramListener(self.story_state,
        #                                             hist_sync_sg,
        #                                             classes_summary_data,
        #                                             scatter_sync_sg, 
        #                                             meas_data)

        # def hist_selection_activate():
        #     if self.histogram_listener.source is not None:
        #         self.session.edit_subset_mode.edit_subset = [self.histogram_listener.source_group]
        #     self.histogram_listener.listen()
        # def hist_selection_deactivate():
        #     self.session.edit_subset_mode.edit_subset = []
        #     self.histogram_listener.ignore()
        # extend_tool(class_distr_viewer, 'bqplot:xrange', hist_selection_activate, hist_selection_deactivate)

        # # We want the hub_fit_viewer to be selecting for the same subset as the table
        # def fit_selection_activate():
        #     self.session.edit_subset_mode.edit_subset = [self.get_widget('fit_table').subset_group]
        # def fit_selection_deactivate():
        #     self.session.edit_subset_mode.edit_subset = []
        # for tool_id in ['bqplot:xrange', 'bqplot:yrange', 'bqplot:rectangle', 'bqplot:circle']:
        #     extend_tool(fit_viewer, tool_id, fit_selection_activate, fit_selection_deactivate)
