from pathlib import Path

from astropy.coordinates import SkyCoord
from astropy.modeling import models, fitting
import astropy.units as u
from bqplot import PanZoom
from echo import CallbackProperty, DictCallbackProperty
from echo.core import add_callback
from glue.core import Component, Data
from glue.core.state_objects import State
from glue_jupyter.app import JupyterApplication
from glue_jupyter.bqplot import scatter
from glue_jupyter.bqplot.histogram import BqplotHistogramView
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.state_traitlets_helpers import GlueState
from glue_wwt.viewer.jupyter_viewer import WWTJupyterViewer
from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from numpy import array, pi, isnan
from pywwt.jupyter import WWTJupyterWidget
from traitlets import Dict, List
import ipyvuetify as v

from cosmicds.components.measuring_tool.measuring_tool import MeasuringTool

from .components.footer import Footer
# When we have multiple components, change above to
# from .components import *
from .components.viewer_layout import ViewerLayout
from .histogram_listener import HistogramListener
from .line_draw_handler import LineDrawHandler
from .utils import MILKY_WAY_SIZE_MPC, age_in_gyr, extend_tool, format_fov, format_measured_angle, line_mark, load_template, update_figure_css, vertical_line_mark
from .components.dialog import Dialog
from .components.table import Table
from .viewers.spectrum_view import SpectrumView

MEASUREMENT_THRESHOLD = 1800 # arcseconds

v.theme.dark = True
v.theme.themes.dark.primary = 'colors.lightBlue.darken3'
v.theme.themes.light.primary = 'colors.lightBlue.darken3'
v.theme.themes.dark.secondary = 'colors.lightBlue.darken4'
v.theme.themes.light.secondary = 'colors.lightBlue.darken4'
v.theme.themes.dark.accent = 'colors.amber.accent2'
v.theme.themes.light.accent = 'colors.amber.accent3'
v.theme.themes.dark.info = 'colors.deepOrange.darken3'
v.theme.themes.light.info = 'colors.deepOrange.lighten2'
v.theme.themes.dark.success = 'colors.green.accent2'
v.theme.themes.light.success = 'colors.green.accent2'
v.theme.themes.dark.warning = 'colors.lightBlue.darken4'
v.theme.themes.light.warning = 'colors.lightBlue.lighten4'
v.theme.themes.dark.anchor = ''
v.theme.themes.light.anchor = ''


# Within ipywidgets - update calls only happen in certain instances.
# Tom added this glue state to allow 2-way binding and force communication that we want explicitly controlled between front end and back end.
class ApplicationState(State):
    # set the darkmode state
    darkmode = CallbackProperty(1)
    marker = CallbackProperty('exp_sky1')

    over_model = CallbackProperty(1)
    col_tab_model = CallbackProperty(0)
    est_model = CallbackProperty(0)
    analysis_tabs = CallbackProperty(0)

    # expansion toggle
    toggle_on = CallbackProperty('d-none')
    toggle_off = CallbackProperty('d-block')

    gal_snackbar = CallbackProperty(0)
    dist_snackbar = CallbackProperty(0)
    marker_snackbar = CallbackProperty(0)
    vel_snackbar = CallbackProperty(0)
    data_ready_snackbar = CallbackProperty(0)

    gal_selected = CallbackProperty(0)
    dist_measured = CallbackProperty(0)
    marker_set = CallbackProperty(0)
    vel_measured = CallbackProperty(0)
    adddata_disabled = CallbackProperty(1)
    prev1_disabled = CallbackProperty(1)
    next1_disabled = CallbackProperty(1)

    gals_total = CallbackProperty(0)
    vels_total = CallbackProperty(0)

    haro_on = CallbackProperty("d-none")
    galaxy_vel = CallbackProperty("")

    calc_visible = CallbackProperty("d-none")

    #step 1 alerts
    wwt_active = CallbackProperty(0)
    galaxy_table_visible = CallbackProperty(0)
    
    spectrum_tool_visible = CallbackProperty(0)

    #state variables for reflections
    rv1_visible = CallbackProperty(0)

    draw_on = CallbackProperty(0)
    bestfit_on = CallbackProperty(0)
    bestfit_drawn = CallbackProperty(False)
    points_plotted = CallbackProperty(False)

    hubble_comparison_selections = CallbackProperty([0])
    class_histogram_selections = CallbackProperty([0])
    alldata_histogram_selections = CallbackProperty([0,1])
    sandbox_histogram_selections = CallbackProperty([0])
    hubble_prodata_selections = CallbackProperty([0])

    morphology_selections = CallbackProperty([0,1,2])

    measured_ang_size_str = CallbackProperty("-")
    measured_ang_size = CallbackProperty(0)
    measuring_on = CallbackProperty(False)
    measure_gal_selected = CallbackProperty(False)
    measuring_name = CallbackProperty("")
    measuring_type = CallbackProperty("")
    measuring_tool_height = CallbackProperty("")
    measuring_view_changing = CallbackProperty(False)
    warn_size = CallbackProperty(False)
    galaxy_dist = CallbackProperty("")

    fit_slopes = DictCallbackProperty()


# Everything in this class is exposed directly to the app.vue.
class Application(VuetifyTemplate):
    _metadata = Dict({"mount_id": "content"}).tag(sync=True)
    state = GlueState().tag(sync=True)
    template = load_template("app.vue", __file__).tag(sync=True)
    viewers = Dict().tag(sync=True, **widget_serialization)
    items = List().tag(sync=True)
    vue_components = Dict().tag(sync=True, **widget_serialization)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state = ApplicationState()
        self._application_handler = JupyterApplication()

        # State callbacks
        add_callback(self.state, 'hubble_comparison_selections', self._hubble_comparison_selection_update)
        add_callback(self.state, 'class_histogram_selections', self._class_histogram_selection_update)
        add_callback(self.state, 'alldata_histogram_selections', self._alldata_histogram_selection_update)
        add_callback(self.state, 'sandbox_histogram_selections', self._sandbox_histogram_selection_update)
        add_callback(self.state, 'morphology_selections', self._morphology_selection_update)
        add_callback(self.state, 'hubble_prodata_selections', self._hubble_prodata_selection_update)

        # Load the galaxy position data
        # This adds the file to the glue data collection at the top level
        data_dir = Path(__file__).parent / "data"
        output_dir = data_dir / "hubble_simulation" / "output"
        self._application_handler.load_data(str(data_dir / "galaxy_data.csv"), 
            label='galaxy_data')
        self._application_handler.load_data(str(data_dir / "Hubble 1929-Table 1.csv"),
            label='Hubble 1929-Table 1')
        self._application_handler.load_data(str(data_dir / "HSTkey2001.csv"),
            label='HSTkey2001') 

        # Load some simulated measurements as summary data
        datasets =[
            "HubbleData_ClassSample",
            "HubbleData_All",
            "HubbleSummary_ClassSample",
            "HubbleSummary_Students",
            "HubbleSummary_Classes",
        ]
        for dataset in datasets:
            self._application_handler.load_data(str(output_dir / f"{dataset}.csv"), label=dataset)

        dummy_redshifts = [0.0119968, 0.00461038, 0.0251682, 0.0271153, 0.0467325]
        self._dummy_student_data = {
            'gal_name': ['2.8205120973628E+018', '1.98723291005848E+018', '2.57949062495682E+018', '2.93425410635467E+018', '1.64172292008027E+018'],
            'element': ['H-alpha', 'Ca K', 'H-alpha', 'H-alpha', 'H-alpha'],
            'measwave': [661.7, 580.0, 725.6, 666.6, 676.8],
            'student_id': [1, 1, 1, 1, 1],
            'distance': [36.3, 80.89, 195.45, 58.61, 144.34],
            'ra_deg': [175.058075, 183.9847263, 139.9247131, 203.3716431, 195.7057343],
            'dec_deg': [24.69706345, 14.43303874, 24.55243683, 17.47060966, 43.21479034],
            'type': ['spiral', 'elliptical', 'irregular', 'spiral', 'elliptical']
        }
        self._dummy_student_data['restwave'] = [round(m/(1+z),2) for m,z in zip(self._dummy_student_data['measwave'], dummy_redshifts)]

        # Calculate the velocities from the wavelengths
        self._dummy_student_data['velocity'] = [round((3*(10**5)) * (o - r) / r, 0) for o,r in zip(self._dummy_student_data['measwave'], self._dummy_student_data['restwave'])]
        self._dummy_galaxy_counter = 0
        self._dummy_distance_counter = 0

        # Instantiate the initial viewers
        spectrum_viewer = self._application_handler.new_data_viewer(
            SpectrumView, data=None, show=False)

        self._application_handler.load_data(str(data_dir / "spectra" / 
            "SDSS_J143450.62+033842.5_S.ecsv"))

        spectrum_viewer.add_data("SDSS_J143450.62+033842.5_S")

        data = self.data_collection['SDSS_J143450.62+033842.5_S']
        # spectrum_viewer.state.x_att = data.id['wavelength']
        spectrum_viewer.layers[0].state.attribute = data.id['flux']

        # Scatter viewers used for the display of the measured galaxy data
        hub_viewers = [self._application_handler.new_data_viewer(BqplotScatterView, data=None, show=False) for _ in range(6)]
        hub_const_viewer, hub_fit_viewer, hub_comparison_viewer, hub_students_viewer, hub_morphology_viewer, hub_prodata_viewer = hub_viewers
        self._hub_viewers = hub_viewers
        for viewer in hub_viewers:
            figure = viewer.figure
            figure.legend_location = 'top-left'
            figure.legend_style = {
                'stroke-width': 0
            }

        # Set up glue links for the Hubble data sets
        measurement_data_fields = self._dummy_student_data.keys()
        table_columns_map = {
            'gal_name' : 'Galaxy Name',
            'element' : 'Element',
            'restwave' : 'Rest Wavelength (nm)',
            'measwave' : 'Observed Wavelength (nm)',
            'velocity' : 'Velocity (km/s)',
            'distance' : 'Distance (Mpc)',
            'type' : 'Galaxy Type'
        }
        self._galaxy_table_components = ['gal_name', 'element', 'restwave', 'measwave', 'velocity']
        galaxy_table_names = [table_columns_map[x] for x in self._galaxy_table_components]
        self._distance_table_components = ['gal_name', 'velocity', 'distance']
        distance_table_names = [table_columns_map[x] for x in self._distance_table_components]
        self._fit_table_components = ['gal_name', 'type', 'velocity', 'distance']
        fit_table_names = [table_columns_map[x] for x in self._fit_table_components]

        measurement_data = Data(label='student_measurements', **{x : array([], dtype='float64') for x in measurement_data_fields})
        class_data = self.data_collection['HubbleData_ClassSample']
        all_data = self.data_collection['HubbleData_All']
        self._measurement_data = measurement_data
        self.data_collection.append(measurement_data)
        for component in class_data.components:
            field = component.label
            self._application_handler.add_link(class_data, field, all_data, field)
        
        # These zero values are dummies; we'll update them later
        dummy_data = {x : ['X'] if x in ['gal_name', 'element', 'type'] else [0] for x in table_columns_map.keys()}
        student_data = Data(label='student_data', **dummy_data)
        self.data_collection.append(student_data)
        for component in class_data.components:
            field = component.label
            if field in student_data.component_ids():
                self._application_handler.add_link(student_data, field, class_data, field)
        
        viewers = [hub_const_viewer, hub_fit_viewer, hub_comparison_viewer, hub_students_viewer]
        for viewer in viewers:
            viewer.add_data(student_data)
            viewer.layers[-1].state.visible = False # We don't want the points to show until the student hits a button
            viewer.state.x_att = student_data.id['distance']
            viewer.state.y_att = student_data.id['velocity']

        # Set up the line fit handler
        self._line_draw_handler = LineDrawHandler(self, hub_fit_viewer)
        self._original_hub_fit_interaction = hub_fit_viewer.figure.interaction

        # Set up the measuring tool
        measuring_widget = WWTJupyterWidget(hide_all_chrome=True)
        measuring_widget.background = 'Digitized Sky Survey (Color)'
        measuring_widget.foreground = 'SDSS: Sloan Digital Sky Survey (Optical)'
        measuring_tool = MeasuringTool(measuring_widget)
        def update_state_ang_size(change):
            ang_size = change["new"]
            ang_size_deg = ang_size.value if self.state.measuring_on else 0
            ang_size_asec = int(ang_size_deg * 3600)
            self.state.measured_ang_size = ang_size_asec
            self.state.measured_ang_size_str = format_measured_angle(ang_size) if ang_size_deg != 0 else "-"
        measuring_tool.observe(update_state_ang_size, names=["angular_size"])
        def update_state_measuring(change):
            self.state.measuring_on = change["new"]
            self.state.warn_size = False
        def update_measuring_height(change):
            self.state.measuring_tool_height = format_fov(change["new"])
        def update_measuring_view_changing(change):
            self.state.measuring_view_changing = change["new"]
        self.state.measuring_tool_height = format_fov(measuring_tool.angular_height)
        measuring_tool.observe(update_measuring_height, names=["angular_height"])
        measuring_tool.observe(update_state_measuring, names=["measuring"])
        measuring_tool.observe(update_measuring_view_changing, names=["view_changing"])
        self.motions_left = 2

        # Load the vue components through the ipyvuetify machinery. We add the
        # html tag we want and an instance of the component class as a
        # key-value pair to the components dictionary.
        velocity_title = 'My Galaxies | Velocity Measurements'
        distance_title = 'My Galaxies | Distance Measurements'
        fit_title = 'My Galaxies'
        self.components = {'c-footer': Footer(self),
                            'c-galaxy-table': Table(self.session, measurement_data, glue_components=self._galaxy_table_components,
                                key_component='gal_name', names=galaxy_table_names, title=velocity_title, single_select=True),
                            'c-distance-table': Table(self.session, measurement_data, glue_components=self._distance_table_components,
                                key_component='gal_name', names=distance_table_names, title=distance_title, single_select=True),
                            'c-fit-table': Table(self.session, student_data, glue_components=self._fit_table_components,
                                key_component='gal_name', names=fit_table_names, title=fit_title),
                            'c-measuring-tool': measuring_tool,
                        # THE FOLLOWING REPLACED WITH video_dialog.vue component in data/vue_components
                        #    'c-dialog-vel': Dialog(
                        #        self,
                        #        launch_button_text="Learn more",
                        #        title_text="How do we measure galaxy velocity?",
                        #        content_text="Verbiage about comparing observed & rest wavelengths of absorption/emission lines",
                        #        accept_button_text="Close"),
                        #    'c-dialog-age': Dialog(
                        #        self,
                        #        launch_button_text="Learn more",
                        #        title_text="How do we estimate age of the universe?",
                        #        content_text="Verbiage about how the slope of the Hubble plot is the inverse of the age of the universe.",
                        #        accept_button_text="Close")
        }

        # Set up the scatter viewers
        default_style_path = str(Path(__file__).parent / "data" /
                                        "styles" / "default_scatter.json")
        comparison_style_path = str(Path(__file__).parent / "data" /
                                        "styles" / "comparison_scatter.json")
        prodata_style_path = str(Path(__file__).parent / "data" /
                                        "styles" / "prodata_scatter.json")
        for viewer in hub_viewers[:-3]:

            # Update the viewer CSS
            update_figure_css(viewer, style_path=default_style_path)
        
        # Set up the viewer that will listen to the histogram
        hub_students_viewer.add_data(class_data)
        hub_students_viewer.state.x_att = class_data.id['distance']
        hub_students_viewer.state.y_att = class_data.id['velocity']
        hub_students_viewer.layers[-1].state.zorder = 2
        update_figure_css(hub_students_viewer, style_path=comparison_style_path)

        # The Hubble comparison viewer should get the class and all public data as well
        all_data = self.data_collection['HubbleData_All']
        hub_comparison_viewer.layers[-1].state.zorder = 3
        hub_comparison_viewer.add_data(class_data)
        hub_comparison_viewer.layers[-1].state.zorder = 2
        hub_comparison_viewer.add_data(all_data)
        hub_comparison_viewer.layers[-1].state.zorder = 1
        hub_comparison_viewer.state.x_att = all_data.id['distance']
        hub_comparison_viewer.state.y_att = all_data.id['velocity']
        hub_comparison_viewer.state.reset_limits()
        update_figure_css(hub_comparison_viewer, style_path=comparison_style_path)

        # Set up the professional data viewer
        hubble1929 = self.data_collection["Hubble 1929-Table 1"]
        hstkp_data = self.data_collection["HSTkey2001"]
        self._application_handler.add_link(hubble1929, 'Distance (Mpc)', hstkp_data, 'Distance (Mpc)')
        self._application_handler.add_link(hubble1929, 'Tweaked Velocity (km/s)', hstkp_data, 'Velocity (km/s)')
        self._application_handler.add_link(hstkp_data, 'Distance (Mpc)', student_data, 'distance')
        self._application_handler.add_link(hstkp_data, 'Velocity (km/s)', student_data, 'velocity')
        hub_prodata_viewer.add_data(student_data)
        hub_prodata_viewer.state.x_att = student_data.id['distance']
        hub_prodata_viewer.state.y_att = student_data.id['velocity']
        hub_prodata_viewer.add_data(hstkp_data)
        hub_prodata_viewer.add_data(hubble1929)
        
        update_figure_css(hub_prodata_viewer, style_path=prodata_style_path)

        # For convenience, we attach the relevant data sets to the application instance
        self._student_data = student_data
        self._class_data = class_data
        self._measurement_data = measurement_data
        self._all_data = all_data
        self._hubble1929 = hubble1929
        self._hstkp_data = hstkp_data

        # Link the age components of the summary data sets
        self._application_handler.add_link(self.data_collection['HubbleSummary_Students'], 'age', self.data_collection['HubbleSummary_Classes'], 'age')
        self._application_handler.add_link(self.data_collection['HubbleSummary_ClassSample'], 'age', self.data_collection['HubbleSummary_Classes'], 'age')

        # Scatter viewer used for the galaxy selection
        gal_viewer = self._application_handler.new_data_viewer(
            BqplotScatterView, data=self.data_collection['galaxy_data'],
            show=False)

        # Histogram viewers for age distribution
        age_distr_viewers = [self._application_handler.new_data_viewer(BqplotHistogramView, data=None, show=False) for _ in range(3)]
        class_distr_viewer, all_distr_viewer, sandbox_distr_viewer = age_distr_viewers

        # Set the axis labels
        for viewer in age_distr_viewers:
            viewer.figure.axes[1].label = 'Count' if viewer == class_distr_viewer else 'Proportion' # maybe something else?

        # The class distribution viewer and the 'sandbox' histogram viewer
        # both need the data for students in the class
        for viewer in [class_distr_viewer, sandbox_distr_viewer]:
            viewer.add_data(self.data_collection["HubbleSummary_ClassSample"])
            viewer.layers[-1].state.color = 'red'
            viewer.figure.marks[-1].opacities = [0.5]

        # The histogram viewer that shows the overall distribution
        # and the 'sandbox' histogram viewer both need the summary data
        # for all students and classes
        for viewer in [all_distr_viewer, sandbox_distr_viewer]:
            viewer.add_data(self.data_collection['HubbleSummary_Students'])
            viewer.layers[-1].state.color = 'blue'
            viewer.figure.marks[-1].opacities = [0.5]
            viewer.add_data(self.data_collection['HubbleSummary_Classes'])
            viewer.figure.marks[-1].opacities = [0.5]
            viewer.layers[-1].state.color = '#f0c470'
            viewer.state.normalize = True
            viewer.state.y_min = 0
            viewer.state.y_max = 1
            viewer.state.hist_n_bin = 30

        # Set all of the histogram viewers to use age as the distribution attribute
        class_distr_viewer.state.x_att = self.data_collection["HubbleSummary_ClassSample"].id['age']
        all_distr_viewer.state.x_att = self.data_collection["HubbleSummary_Students"].id['age']
        sandbox_distr_viewer.state.x_att = self.data_collection["HubbleSummary_Students"].id['age']

        # Set up the subsets in the morphology viewer
        galaxy_data = self.data_collection['galaxy_data']
        elliptical_subset = galaxy_data.new_subset(galaxy_data.id['MorphType'] == 'E', label='Elliptical', color='orange')
        spiral_subset = galaxy_data.new_subset(galaxy_data.id["MorphType"] == 'Sp', label='Spiral', color='green')
        irregular_subset = galaxy_data.new_subset(galaxy_data.id["MorphType"] == 'Ir', label='Irregular', color='red')
        morphology_subsets = [elliptical_subset, spiral_subset, irregular_subset]
        for subset in morphology_subsets:
            hub_morphology_viewer.add_subset(subset)
        self._elliptical_subset = elliptical_subset
        self._spiral_subset = spiral_subset
        self._irregular_subset = irregular_subset
        hub_morphology_viewer.state.x_att = self.data_collection['galaxy_data'].id['EstDist_Mpc']
        hub_morphology_viewer.state.y_att = self.data_collection['galaxy_data'].id['velocity_km_s']
        update_figure_css(hub_morphology_viewer, style_path=default_style_path)

        # Set up the listener to sync the histogram <--> scatter viewers
        meas_data = self.data_collection["HubbleData_ClassSample"]
        summ_data = self.data_collection["HubbleSummary_ClassSample"]
        hist_sync_sg = self.data_collection.new_subset_group(label="Hist Sync SG")
        scatter_sync_sg = self.data_collection.new_subset_group(label="Scatter Sync SG")
        hist_sync_sg.style.color = "green"
        scatter_sync_sg.style.color = "green"

        # Right now, this is the only viewer aside from the synced viewers
        # that shows these data objects
        for layer in sandbox_distr_viewer.layers:
            if layer.state.layer.label in [hist_sync_sg.label, scatter_sync_sg.label]:
                layer.state.visible = False

        
        # Set up the functionality for the histogram <---> scatter sync
        # We add a listener for when a subset is modified/created on 
        # the histogram viewer as well as extend the xrange tool for the 
        # histogram to always affect this subset
        #hub_students_viewer.layers[-1].state.color = "#ff0000"
        self._histogram_listener = HistogramListener(self,
                                                     hist_sync_sg,
                                                     summ_data,
                                                     scatter_sync_sg, 
                                                     meas_data)

        def hist_selection_activate():
            if self._histogram_listener.source is not None:
                self.session.edit_subset_mode.edit_subset = [self._histogram_listener.source_group]
            self._histogram_listener.listen()
        def hist_selection_deactivate():
            self.session.edit_subset_mode.edit_subset = []
            self._histogram_listener.ignore()
        extend_tool(class_distr_viewer, 'bqplot:xrange', hist_selection_activate, hist_selection_deactivate)

        # We want the hub_fit_viewer to be selecting for the same subset as the table
        def hub_fit_selection_activate():
            self.session.edit_subset_mode.edit_subset = [self.components['c-fit-table'].subset_group]
        def hub_fit_selection_deactivate():
            self.session.edit_subset_mode.edit_subset = []
        for tool_id in ['bqplot:xrange', 'bqplot:yrange', 'bqplot:rectangle', 'bqplot:circle']:
            extend_tool(hub_fit_viewer, tool_id, hub_fit_selection_activate, hub_fit_selection_deactivate)

        # Set the data for the screen 3 table to be the completed measurements data
        # and create a subset for the table component.
        # Finally, hide this subset everywhere but screen 3.
        # We want to do the same for the distance table
        for table_id in ['c-fit-table', 'c-distance-table']:
            table = self.components[table_id]
            subset_group_label = table_id[2:] + '-selected'
            subset_group = self.data_collection.new_subset_group(label=subset_group_label, subset_state=None)
            table.subset_group = subset_group
            for viewer in hub_viewers + age_distr_viewers + [spectrum_viewer]:
                for layer in viewer.layers:
                    if layer.state.layer.label == subset_group.label:
                        layer.state.visible = False

        # When we select an item in the distance table, we want the WWT viewer to go there
        distance_table = self.components['c-distance-table']
        def distance_table_selected_changed(change):
            table = self.components['c-distance-table']
            selected = change["new"]
            state = table.subset_state_from_selected(selected)
            mask = state.to_mask(table.glue_data)
            ra = next((x for index, x in enumerate(table.glue_data["ra_deg"]) if mask[index]), None)
            dec = next((x for index, x in enumerate(table.glue_data["dec_deg"]) if mask[index]), None)
            gal_type = next((x for index, x in enumerate(table.glue_data["type"]) if mask[index]), None)
            self.state.measure_gal_selected = len(selected) > 0
            self.components['c-measuring-tool'].reset_canvas()
            if not self.state.measure_gal_selected:
                self.state.measuring_name = None
                self.state.measuring_type = None
                return
            name = selected[0]["gal_name"]
            if ra is not None and dec is not None:
                measuring_tool = self.components['c-measuring-tool']
                widget = measuring_tool.widget
                coordinates = SkyCoord(ra * u.deg, dec * u.deg, frame='icrs')
                ## TODO: Once we have it, specify the correct fov for each point
                use_instant = self.motions_left <= 0
                widget.center_on_coordinates(coordinates, fov=0.016 * u.deg, instant=use_instant)
                if not use_instant:
                    self.motions_left -= 1
                self.state.measuring_name = name
                self.state.measuring_type = gal_type.capitalize()
            
        distance_table.observe(distance_table_selected_changed, names=['selected'])

        # TO DO: Currently, the glue-wwt package requires qt binding even if we
        #  only intend to use the juptyer viewer.
        wwt_viewer = self._application_handler.new_data_viewer(
            WWTJupyterViewer, data=self.data_collection['galaxy_data'], show=False)

        data = self.data_collection['galaxy_data']
        wwt_viewer.state.lon_att = data.id['RA_deg']
        wwt_viewer.state.lat_att = data.id['Dec_deg']

        # Any lines that we've obtained from fitting
        # Entries have the form (line, data label)
        # These are keyed by viewer id
        self._fit_lines = {}

        # The slopes that we've fit to any data sets
        # This is keyed by the label of the data
        self._fit_slopes = {}

        # Any vertical line marks on histograms
        # keyed by viewer id
        self._histogram_lines = {}

        # scatter_viewer_layout = vuetify_layout_factory(gal_viewer)

        # Store an internal collection of the glue viewer objects
        self._viewer_handlers = {
            'spectrum_viewer': spectrum_viewer, 
            'gal_viewer': gal_viewer,
            'hub_const_viewer': hub_const_viewer,
            'hub_comparison_viewer': hub_comparison_viewer,
            'hub_students_viewer': hub_students_viewer,
            'hub_fit_viewer': hub_fit_viewer,
            'hub_morphology_viewer': hub_morphology_viewer,
            'hub_prodata_viewer': hub_prodata_viewer,
            'wwt_viewer': wwt_viewer,
            'class_distr_viewer': class_distr_viewer,
            'all_distr_viewer': all_distr_viewer,
            'sandbox_distr_viewer': sandbox_distr_viewer,
        }

        # Store a front-end accessible collection of renderable ipywidgets
        self.viewers = { k : ViewerLayout(v) for k, v in self._viewer_handlers.items() }

        # Make sure that the initial layer visibilities match the state
        self._hubble_comparison_selection_update(self.state.hubble_comparison_selections)
        self._class_histogram_selection_update(self.state.class_histogram_selections)
        self._alldata_histogram_selection_update(self.state.alldata_histogram_selections)
        self._sandbox_histogram_selection_update(self.state.sandbox_histogram_selections)
        self._morphology_selection_update(self.state.morphology_selections)
        self._hubble_prodata_selection_update(self.state.hubble_prodata_selections)

        self._application_handler.set_subset_mode('replace')

        # Set the bottom-left corner of the plot to be the origin in each scatter viewer
        for viewer in hub_viewers:
            viewer.state.x_min = 0
            viewer.state.y_min = 0

        if kwargs.get('test', False):
            self._testing_add_data()


    def reload(self):
        """
        Reload only the UI elements of the application.
        """
        self.template = load_template("app.vue", __file__, traitlet=False)

    @property
    def session(self):
        """
        Underlying glue-jupyter application session instance.
        """
        return self._application_handler.session

    @property
    def data_collection(self):
        """
        Underlying glue-jupyter application data collection instance.
        """
        return self._application_handler.data_collection

    def vue_toggle_darkmode(self, args):
        v.theme.dark = not v.theme.dark

    def vue_fit_lines(self, args):
        """
        This function handles line fitting, with the specifics of the fitting
        controlled by the arguments.

        Parameters
        ----------
        args: dict
            A dictionary of arguments, with following entries:

        viewer_id : str
            The identifier for the viewer to use.
        layers : List[int]
            (Optional) A list of the indices of the layers that should be fit to. 
            If not specified, a line is fit for every layer present in 
            the viewer.
        clear_others: bool
            (Optional) If true, all old lines present on this viewer will be cleared.
            Otherwise, only old lines for the selected data ids will be cleared;
            lines for other layers will be left as they are. Default is False.
        aggregate: bool
            (Optional) If true, the data for all specified layers is concatenated and a
            single fit is done for the combined data. Otherwise, a separate fit
            is done for each layer. Default is False.
        """

        viewer_id = args['viewer_id']
        layer_indices = args.get('layers')
        clear_others = args.get('clear_others') or False
        aggregate = args.get('aggregate') or False
        viewer = self._viewer_handlers[viewer_id]

        if layer_indices is None:
            layer_indices = list(range(len(viewer.layers)))
        layers = [layer for index, layer in enumerate(viewer.layers) if layer.state.visible and index in layer_indices]
        
        if aggregate:
            self._fit_lines_aggregate(viewer_id, layers, clear_others)
        else:
            self._fit_lines_layers(viewer_id, layers, clear_others)

    def _fit_lines_layers(self, viewer_id, layers, clear_others=False):
        viewer = self._viewer_handlers[viewer_id]
        figure = viewer.figure

        data_labels = [layer.state.layer.label for layer in layers]

        lines_and_labels = []
        for layer in layers:

            # Get the data (which may actually be a Data object,
            # or represent a subset)
            data = layer.state.layer
            if data.size <= 1: # We need at least 2 points for a line
                continue

            # Do the line fit
            x_arr = data[viewer.state.x_att]
            y_arr = data[viewer.state.y_att]
            fit = fitting.LinearLSQFitter()
            line_init = models.Linear1D(intercept=0, fixed={'intercept':True})
            fitted_line = fit(line_init, x_arr, y_arr)
            x = [0, 2*viewer.state.x_max] # For now, the line spans from 0 to twice the edge of the viewer
            y = fitted_line(x)

            # Create the fit line object
            # Keep track of this line and its slope
            start_x, end_x = x
            start_y, end_y = y
            slope_value = fitted_line.slope.value
            label = 'Slope = %.0f ks / s / Mpc' % slope_value if not isnan(slope_value) else None
            line = line_mark(layer, start_x, start_y, end_x, end_y, layer.state.color, label)
            lines_and_labels.append((line, data.label))
            
            # Keep track of this slope for later use
            self.state.fit_slopes[data.label] = fitted_line.slope.value

        # Order the lines in the same order as the layers
        lines_and_labels.sort(key=lambda x: data_labels.index(x[1]), reverse=True)
        lines, labels = [*zip(*lines_and_labels)]

        # Since the glupyter viewer doesn't have an option for lines
        # we just draw the fit lines directly onto the bqplot figure
        # If we previously drew any lines in this viewer, remove them
        old_items = self._fit_lines.get(viewer_id, [])
        to_clear, to_keep = [], []
        for item in old_items:
            if clear_others or (item[1] in data_labels):
                to_clear.append(item)
            else:
                to_keep.append(item)
        marks_to_clear = [x[0] for x in to_clear]
        marks_to_keep = [x for x in figure.marks if x not in marks_to_clear]
        figure.marks = marks_to_keep + list(lines)
        self._fit_lines[viewer_id] = to_keep + lines_and_labels

    def _fit_lines_aggregate(self, viewer_id, layers, clear_others=False):
        viewer = self._viewer_handlers[viewer_id]
        figure = viewer.figure

        x, y = [], []
        for layer in layers:

            # Get the data (which may actually be a Data object,
            # or represent a subset
            data = layer.state.layer

            # Do the line fit
            x_arr = data[viewer.state.x_att]
            y_arr = data[viewer.state.y_att]
            x.extend(list(x_arr))
            y.extend(list(y_arr))

        fit = fitting.LinearLSQFitter()
        line_init = models.Linear1D(intercept=0, fixed={'intercept':True})
        fitted_line = fit(line_init, x, y)
        x = [0, 2*viewer.state.x_max] # For now, the line spans from 0 to twice the edge of the viewer
        y = fitted_line(x)

        # Create the fit line object
        # Keep track of this line and its slope
        start_x, end_x = x
        start_y, end_y = y
        slope_value = fitted_line.slope.value
        label = 'Slope = %.0f km / s /  Mpc' % slope_value if not isnan(slope_value) else None
        line = line_mark(layers[0], start_x, start_y, end_x, end_y, 'black', label)
        self.state.fit_slopes['aggregate_%s' % viewer_id] = fitted_line.slope.value

         # Since the glupyter viewer doesn't have an option for lines
        # we just draw the fit line directly onto the bqplot figure
        # If we previously drew any lines in this viewer, remove them
        old_items = self._fit_lines.get(viewer_id, [])
        to_clear, to_keep = [], []
        for item in old_items:
            if clear_others or (item[1] == 'aggregate'):
                to_clear.append(item)
            else:
                to_keep.append(item)
        marks_to_clear = [x[0] for x in to_clear]
        marks_to_keep = [x for x in figure.marks if x not in marks_to_clear]
        figure.marks = marks_to_keep + [line]
        self._fit_lines[viewer_id] = to_keep + [(line, 'aggregate')]

    def vue_clear_lines(self, viewer_id, layer_indices=None):
        """
        "Clears all fit lines for the given viewer.
        """
        viewer = self._viewer_handlers[viewer_id]
        figure = viewer.figure

        old_items = self._fit_lines.get(viewer_id, [])

        if layer_indices is None:
            to_remove = [x[0] for x in old_items]
        else:
            labels = [viewer.layers[i].state.layer.label for i in layer_indices]
            to_remove = [x[0] for x in old_items if x[1] in labels]

        figure.marks = [mark for mark in figure.marks if mark not in to_remove]
        self._fit_lines[viewer_id] = []

    def vue_add_data_to_viewers(self, viewer_ids):
        for viewer_id in viewer_ids:
            viewer = self._viewer_handlers[viewer_id]
            if viewer_id == 'hub_const_viewer':
                data = self.data_collection['HubbleData_ClassSample']
                viewer.add_data(data)
                viewer.x_att = data.id['Distance']
                viewer.y_att = data.id['Velocity']
            elif viewer_id == 'wwt_viewer':
                data = self.data_collection['galaxy_data']
                viewer.add_data(data)
                viewer.lon_att = data.id['RA_deg']
                viewer.lat_att = data.id['Dec_deg']
            elif viewer_id == 'age_distr_viewer':
                data = self.data_collection['HubbleSummary_Overall']
                viewer.add_data(data)
                viewer.x_att = data.id['age']

    def _scatter_selection_update(self, viewer_id, data, selections):
        viewer = self._viewer_handlers[viewer_id]
        labels = [x.label for (i,x) in enumerate(data) if i in selections]

        for layer in viewer.layers:
            layer.state.visible = layer.state.layer.label in labels

        # We only want to show lines for the layers that are visible
        line_info = self._fit_lines.get(viewer_id, [])
        all_lines = [x[0] for x in line_info]

        figure = viewer.figure
        not_lines = [mark for mark in figure.marks if mark not in all_lines]
        line_items = [x for x in line_info if x[1] in labels]
        line_items.sort(key=lambda x: labels.index(x[1]))
        lines = [x[0] for x in line_items]
        figure.marks = not_lines + lines

    def _hubble_comparison_selection_update(self, selections):
        # Indices:
        # 0: Student's data
        # 1: Their class's data
        # 2: All public data
        viewer_id = 'hub_comparison_viewer'
        data = [self._student_data, self._class_data, self._all_data, self._histogram_listener.modify_group]
        if 1 in selections:
            selections.append(3)
        self._scatter_selection_update(viewer_id, data, selections)

    def _morphology_selection_update(self, selections):
        # Indices:
        # 0: Elliptical
        # 1: Spiral
        # 2: Irregular
        viewer_id = 'hub_morphology_viewer'
        data = [self._elliptical_subset, self._spiral_subset, self._irregular_subset]
        self._scatter_selection_update(viewer_id, data, selections)

    def _hubble_prodata_selection_update(self, selections):
        # Indices:
        # 0: Student data
        # 1: Hubble 1929
        # 2: HSTKP
        viewer_id = 'hub_prodata_viewer'
        data = [self._student_data, self._hubble1929, self._hstkp_data]
        self._scatter_selection_update(viewer_id, data, selections)

    def _histogram_selection_update(self, selections, viewer_id, line_options=[], layer_mapping=None):
        """
        Callback function to be executed when the selections corresponding to one of
        the histogram viewers is changed.

        Parameters
        ----------
        selections : List[int]
            The indices of the selected options.
        viewer_id : str
            The identifier for the viewer to use.
        layer_mapping : Dict[int,int]
            (Optional) A dictionary mapping the indices of glue layers to the selection
            indices. If not given, the layer at a given index will be mapped to
            the selection option at the same index.
        line_options: List[Tuple[int, float, str]]
            (Optional) A list of tuple of options (index, slope, color) for the vertical
            lines to be plotted.
        """
        viewer = self._viewer_handlers[viewer_id]
        first_layer = viewer.layers[0]

        layer_mapping = layer_mapping or { x : x for x in range(len(viewer.layers)) }
        for index, layer in enumerate(viewer.layers):
            layer.state.visible = layer_mapping.get(index, -1) in selections

        lines = []
        for index, slope, color in line_options:
            if index in selections and slope is not None:
                age = age_in_gyr(slope)
                label = 'Age = %.0f Gyr' % age if not isnan(age) else None
                line = vertical_line_mark(first_layer, age, color, label)
                lines.append(line)

        figure = viewer.figure
        old_lines = self._histogram_lines.get(viewer_id, [])
        figure.marks = [mark for mark in figure.marks if not mark in old_lines] + lines
        self._histogram_lines[viewer_id] = lines

        # We need to do a bit of a hack for the histogram viewer lines
        # Using the same scale object as the viewer image modifies the y-axis for some reason
        # so to get around that, these marks have new scales which mimic the view scales
        # and thus we need to add them to the viewer's PanZoom interaction
        line_scales = [line.scales for line in lines]
        x_scales = [scale['x'] for scale in line_scales]
        y_scales = [scale['y'] for scale in line_scales]

        # If the PanZoom is currently open, we need to update this right now
        if isinstance(figure.interaction.next, PanZoom):
            figure.interaction.next = PanZoom(scales={
                'x': [viewer.scale_x] + x_scales,
                'y': [viewer.scale_y] + y_scales,
            })

        # Observe interaction changes so that we can modify when necessary
        # We want to remove any observers that we have previously set
        figure.interaction.unobserve_all(name='next')
        figure.interaction.observe(lambda changed: self._panzoom_interaction_update(changed, viewer_id), names=['next'])

    def _panzoom_interaction_update(self, change, viewer_id):

        viewer = self._viewer_handlers[viewer_id]
        figure = viewer.figure

        # If the new interaction isn't a PanZoom, no need to do anything
        if not isinstance(change['new'], PanZoom):
            return
        pan_zoom = change['new']

        # No need to update if the scales are exactly the same as those in the PanZoom
        # This also avoids infinite setting loops
        lines = self._histogram_lines.get(viewer_id, [])
        line_scales = [line.scales for line in lines]
        x_scales = [scale['x'] for scale in line_scales]
        y_scales = [scale['y'] for scale in line_scales]
        x_needs_update = not all(scale in pan_zoom.scales['x'] for scale in x_scales)
        y_needs_update = not all(scale in pan_zoom.scales['y'] for scale in y_scales)
        if not (x_needs_update or y_needs_update):
            return

        # Update the interaction
        figure.interaction.next = PanZoom(scales={
            'x': [viewer.scale_x] + x_scales,
            'y': [viewer.scale_y] + y_scales,
        })
            
    def _class_histogram_selection_update(self, selections):
        """
        Specialization of _histogram_selection_update for the case of the class histogram.

        Parameters
        ----------
        selections : List[int]
            The indices of the selected options. The indices in this case represent:
            * 0: Individual students (glue layer)
            * 1: Student's selected subset (glue layer) - only if student has made selection
            * 1 or 2: Student's value (line mark)
            * 2 or 3: Class's value (line mark)
        """

        line_options = [
            (1, self.student_slope, 'blue'),
            (2, self.class_slope, 'green')
        ]
        layer_mapping = { 0 : 0, 1 : 0 } # We hide a selected subset if the glue layer is hidden
        self._histogram_selection_update(selections, 'class_distr_viewer',
            layer_mapping=layer_mapping, line_options=line_options)
    
    def _alldata_histogram_selection_update(self, selections):
        """
        Specialization of _histogram_selection_update for the case of the histogram of all data.

        Parameters
        ----------
        selections : List[int]
            The indices of the selected options. The indices in this case represent:
            * 0: All students (glue layer)
            * 1: All students (glue layer)
        """
        self._histogram_selection_update(selections, 'all_distr_viewer')
    
    def _sandbox_histogram_selection_update(self, selections):
        """
        Specialization of _histogram_selection_update for the case of the final 'sandbox' histogram.

        Parameters
        ----------
        selections : List[int]
            The indices of the selected options. The indices in this case represent:
            * 0: Students in the class (glue layer)
            * 1: All students (glue layer)
            * 2: Students from all classes (glue layer)
            * 3: This class's age (line mark)
            * 4: Age from all data (line mark)
            * 5: Student's age (line mark)
        """
        line_options = [
            (3, self.class_slope, 'purple'),
            (4, self.all_slope, 'green'),
            (5, self.student_slope, 'black')
        ]
        self._histogram_selection_update(selections, 'sandbox_distr_viewer', line_options=line_options)

    def vue_clear_histogram_selection(self, _args):
        toolbar = self._viewer_handlers['class_distr_viewer'].toolbar
        toolbar.active_tool = None
        self._histogram_listener.clear_subset()

    def _update_data_component(self, data, attribute, values):
        if attribute in data.component_ids():
            data.update_components({data.id[attribute] : values})
        else:
            data.add_component(Component.autotyped(values), attribute)
        data.broadcast(attribute)

    def _new_dist_data_update(self, distance):

        # Update the measurement Data object
        label = 'student_measurements'
        data = self.data_collection[label]
        if len(distance) > data.size:
            return

        self._update_data_component(data, 'distance', distance)

        # Create a new Data object from all of the 'finished' data points
        # and update to match that
        df = data.to_dataframe()
        df = df.dropna()

        main_comps = [x.label for x in data.main_components]
        components = { col : list(df[col]) for col in main_comps }
        new_data = Data(label='student_data', **components)

        # Update the data
        self._student_data.update_values_from_data(new_data)

        # If there's a line on the fit viewer, it's now out of date
        # so we clear it
        if self._fit_lines.get('hub_fit_viewer', []):
            self.vue_clear_lines('hub_fit_viewer')

        # Same for a drawn line
        self._line_draw_handler.clear()

        # Update viewer limits and labels
        # We don't want to redo all of the styling,
        # as that is noticeably slow
        viewer_ids = ['hub_fit_viewer', 'hub_comparison_viewer', 'hub_prodata_viewer']
        for viewer_id in viewer_ids:
            viewer = self._viewer_handlers[viewer_id]
            viewer.state.reset_limits()
            viewer.state.x_min = 0
            viewer.state.y_min = 0
            viewer.figure.axes[0].label = "Distance (Mpc)"
            viewer.figure.axes[1].label = "Velocity (km/s)"
        for viewer_id in ['class_distr_viewer', 'all_distr_viewer', 'sandbox_distr_viewer']:
            viewer = self._viewer_handlers[viewer_id]
            viewer.figure.axes[0].label = 'Age (Gyr)'


        #style_files = ["default_scatter.json", "comparison_scatter.json", "prodata_scatter.json"]
        # for viewer_id, style_path in zip(viewer_ids, style_files):
        #     style_path = str(Path(__file__).parent / "data" /
        #                                 "styles" / style_path)
        #     viewer = self._viewer_handlers[viewer_id]
        #     viewer.state.reset_limits()
        #     viewer.state.x_min = 0
        #     viewer.state.y_min = 0
        #     update_figure_css(viewer, style_path=style_path)
        #     print(f"Updated figure CSS for {viewer_id}")
            
    def _new_galaxy_data_update(self, new_data):
        dc = self.data_collection
        label = 'student_measurements'
        data = dc[label]
        data.update_values_from_data(new_data)

    def vue_add_distance_data_point(self, test=False):

        # Is the value that the student measured too large?
        # If so, we give a warning rather than adding this value
        if self.state.measured_ang_size >= MEASUREMENT_THRESHOLD:
            self.state.warn_size = True
            return

        self.state.warn_size = False
        distance_value = round(MILKY_WAY_SIZE_MPC / (self.state.measured_ang_size * pi / (180 * 3600)), 0)
        self.state.galaxy_dist = str(int(distance_value))

        data = self.data_collection['student_measurements']
        if test:
            if self._dummy_distance_counter >= len(self._dummy_student_data['gal_name']):
                return
            distance = self._dummy_student_data['distance'][:self._dummy_distance_counter + 1] + [None]*(data.size - self._dummy_distance_counter - 1)
        else:
            table = self.components['c-distance-table']
            state = table.subset_state_from_selected(table.selected)
            mask = state.to_mask(table.glue_data)
            index = next((index for index in range(len(mask)) if mask[index]), None)
            if index is not None:
                distance = data["distance"]
                distance[index] = distance_value

        self._new_dist_data_update(distance)
        self._dummy_distance_counter += 1
            
    def vue_add_galaxy_data_point(self, _args):
        if self._dummy_galaxy_counter >= len(self._dummy_student_data['gal_name']):
            return

        self._dummy_galaxy_counter += 1
        component_mapping = {
            k : v[:self._dummy_galaxy_counter] for k, v in self._dummy_student_data.items() if k != 'distance'
        }

        if 'student_measurements' in self.data_collection:
            data = self.data_collection['student_measurements']
            distance = list(data['distance']) + [None]
        else:
            distance = [None]*self._dummy_galaxy_counter
        component_mapping['distance'] = distance
        new_data = Data(label='student_measurements', **component_mapping)
        self._new_galaxy_data_update(new_data)

    def vue_show_fit_points(self, _args):
        for viewer in self._hub_viewers:
            for layer in viewer.layers:
                if layer.state.layer.label in [self._student_data.label, self.components['c-fit-table'].subset_group.label]:
                    layer.state.visible = True

    def vue_handle_fitline_click(self, _args):
        if not self.state.bestfit_drawn:
            self.state.draw_on = not self.state.draw_on
        else:
            self._line_draw_handler.clear()

    def _testing_add_data(self):

        # Add the data
        for _ in range(len(self._dummy_student_data['gal_name'])):
            self.vue_add_galaxy_data_point(None)
            self.vue_add_distance_data_point(True)

        # Set the bottom-left corner of the plot to be the origin in each scatter viewer
        for viewer in self._hub_viewers:
            viewer.state.x_min = 0
            viewer.state.y_min = 0

        self.vue_show_fit_points(None)

    def vue_reset_measurer(self, _args):
        self.components['c-measuring-tool'].reset_canvas()

    def vue_toggle_measuring(self, _args):
        measurer = self.components['c-measuring-tool']
        measurer.measuring = not measurer.measuring

    # These three properties provide convenient access to the slopes of the the fit lines
    # for the student's data, the class's data, and all of the data
    @property
    def student_slope(self):
        if not hasattr(self, '_student_data'):
            return 0
        return self.state.fit_slopes.get(self._student_data.label, 0)

    @property
    def class_slope(self):
        return self.state.fit_slopes.get(self._class_data.label, 0)

    @property
    def all_slope(self):
        return self.state.fit_slopes.get(self._all_data.label, 0)
