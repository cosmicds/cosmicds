<template>
  <v-app
    id="cosmicds-app"
  >
    <!-- Tool bar, fixed to the top of the application -->
    <v-app-bar
      color="primary"
      dark
      src="https://cdn.eso.org/images/screen/eso1738b.jpg"
      scroll-target="#scrolling-techniques-4"
    >
      <template
        v-slot:img="{ props }"
      >
        <v-img
          v-bind="props"
          gradient="to top right, rgba(100,115,201,.7), rgba(25,32,72,.7)"
        ></v-img>
      </template>

      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <v-toolbar-title>
        Cosmic Data Stories | Hubble's Law
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- The main section of the application -->
    <v-main
      id="scrolling-techniques-4"
      class="overflow-y-auto fill-height"
    >
      <v-container>
        <v-row justify="center">
          <v-col cols="12" xl="8">
            <v-card class="d-flex flex-column">

            <!-- This sets up the multi-step sections across the top -->
            <!-- v-model is a 2-way token that controls the state of something in the app -->
              <v-stepper
                v-model="state.over_model"
                class="elevation-0"
              >
                <v-stepper-header>
                  <!-- :complete="state.over_model > 1"   
                        : is a binding - binds state of "complete" to the thing in the "".  If over_model is > 1, then we have gone past step 1.
                  therefore, consider step 1 complete. -->
                  <!-- Another example could be something like :disabled = "state.continue_button_disabled==1" -->

                  <v-stepper-step
                    :complete="state.over_model > 1"
                    step="1"
                    editable
                  >
                    Collect<br>Velocity Data
                  </v-stepper-step>

                  <v-divider></v-divider>

                  <v-stepper-step
                    :complete="state.over_model > 2"
                    step="2"
                    editable
                  >
                    Collect<br>Distance Data
                  </v-stepper-step>

                  <v-divider></v-divider>

                  <v-stepper-step
                    :complete="state.over_model > 3"
                    step="3"
                    editable
                  >
                    Estimate<br>Age
                  </v-stepper-step>

                  <v-divider></v-divider>

                  <v-stepper-step
                    :complete="state.over_model > 4"
                    step="4"
                    editable
                    >Explore<br>Class Data
                  </v-stepper-step>

                  <v-divider></v-divider>

                  <v-stepper-step
                    :complete="state.over_model > 5"
                    step="5"
                    editable
                    >View<br>Distributions
                  </v-stepper-step>
                  <v-divider></v-divider>

                <v-stepper-step
                    :complete="state.over_model > 6"
                    step="6"
                    editable
                    >Galaxy<br>Morphology
                  </v-stepper-step>
                  <v-divider></v-divider>
                <v-stepper-step
                    :complete="state.over_model > 7"
                    step="7"
                    editable
                    >Professional<br>Science Data
                  </v-stepper-step>
                </v-stepper-header>

              <!-- This sets up the screen for the galaxy selection/measurement step -->
                <v-stepper-items
                  class=""
                >

                  <!-- ---------------- -------------------------------- ---------------- -->
                  <!-- ---------------- FIRST PAGE: VELOCITY MEASUREMENT ---------------- -->
                  <!-- ---------------- -------------------------------- ---------------- -->
                  <v-stepper-content step="1">
                    <v-container>
                      <v-row>
                        <v-col
                          cols="4"
                        >
                          <!-- WIDGET for WWT galaxy selection -->
                          <v-lazy>
                          <jupyter-widget
                            :widget="viewers.wwt_viewer"
                          ></jupyter-widget>
                          </v-lazy>
                        </v-col>
                        <v-col>
                          <!-- TABLE to hold Selected Galaxies -->
                          <c-galaxy-table/>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-alert
                          class="mb-4"
                          border="left"
                          colored-border
                          color="indigo"
                          elevation="2"
                        >
                          Pan the sky and click one of the markers to 
                          select a galaxy to measure. You will then
                          use emission or absorption lines in its
                          spectrum to measure the galaxy's velocity.
                          NOTE: The button here stands in place of WWT
                          selection function until it becomes available.
                          <!-- This can go because the "select" action will be on the galaxy marker within the WWT window -->
                          <div class="text-center mt-4">
                            <v-btn
                              class="white--text"
                              color="purple darken-2"
                              @click="
                                state.gal_snackbar = 0;
                                state.dist_snackbar = 0;
                                state.marker_snackbar = 0;
                                state.vel_snackbar = 0;
                                state.data_ready_snackbar = 0;
                                state.gal_snackbar = 1;
                                state.gal_selected = 1;
                                state.haro_on = 'd-block';
                                add_galaxy_data_point();
                              "
                            >
                              select galaxy (placeholder function)
                            </v-btn>
                          </div>
                        </v-alert>
                      </v-row>
                    </v-container>
                    <v-container>
                      <v-row>
                        <v-col
                          cols="12" md="8"
                          class="align-stretch"
                        >
                          <v-card
                            min-height="300px"
                            height="100%"
                          >
                            <v-toolbar
                              color="pink"
                              dark
                            >
                              <v-icon left>
                                mdi-speedometer
                              </v-icon>

                              <v-toolbar-title>Measure Velocity</v-toolbar-title>

                              <v-spacer></v-spacer>

                              <v-btn icon>
                                <v-icon>mdi-information-outline</v-icon>
                              </v-btn>
                            </v-toolbar>
                            <v-card-text
                              class="pa-5"
                            >
                              TO DO: New spectrum viewer code here.
                            </v-card-text>
                          </v-card>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-alert
                            border="left"
                            colored-border
                            color="indigo"
                            elevation="2"
                            class="mb-12"
                          >
                          <!-- Our SME told me that E galaxies aren't likely to have H-alpha lines, so we will need to give
                          options for measuring other types of lines too, like Ca or K lines. We can figure this out once
                          we have the data set to look at.-->
                            Use the mouse to drag the vertical wavelength marker
                            until it lines up with the labeled absorption or
                            emission line. Left-click to record the element and
                            wavelength of the line. NOTE: The button here stands
                            in place of wavelength setter function until it
                            becomes available.

                            <!-- Again, I think the click action will be on the spectrum itself, so we can remove this -->
                            <div class="text-center mt-4">
                              <v-btn
                                :disabled="!state.gal_selected"
                                class="white--text"
                                color="purple darken-2"
                                @click="
                                  state.gal_snackbar = 0;
                                  state.dist_snackbar = 0;
                                  state.marker_snackbar = 0;
                                  state.vel_snackbar = 0;
                                  state.data_ready_snackbar = 0;
                                  state.marker_snackbar = 1;
                                  state.marker_set = 1;
                                  state.marker_on = 'd-block'
                                "
                              >
                                set marker
                              </v-btn>
                            </div>
                          </v-alert>

                          <div
                          >
                            <v-card
                              color="indigo lighten-5"
                              clas="mb-4"
                              :disabled="!state.marker_set"
                            >
                              <v-card-text>
                                <v-text-field
                                  :value="state.galaxy_vel"
                                  label="Calculated Velocity"
                                  hint="click button below"
                                  persistent-hint
                                  color="purple darken-2"
                                  class="mb-4"
                                  suffix="km/s"
                                  outlined
                                  readonly
                                  dense
                                ></v-text-field>
                                <v-btn
                                  block
                                  color="purple darken-2"
                                  class="px-auto"
                                  max-width="100%"
                                  dark
                                  @click="
                                    state.gal_snackbar = 0;
                                    state.dist_snackbar = 0;
                                    state.marker_snackbar = 0;
                                    state.vel_snackbar = 0;
                                    state.data_ready_snackbar = 0;
                                    state.vel_measured = 1;
                                    state.dist_measured == 1
                                      ? state.data_ready_snackbar = 1
                                      : state.vel_snackbar = 1;
                                    state.adddata_disabled =
                                      state.dist_measured == 1
                                        ? false
                                        : true
                                    state.galaxy_vel = Math.floor(Math.random() * 60000) + 5000
                                  "
                                >
                                  calculate
                                </v-btn>
                              </v-card-text>
                            </v-card>
                          </div>
                          <v-card
                            outlined
                            class="pa-5 mt-8"
                            color="orange lighten-5"
                            elevation="0"
                          >
                            Watch this video for instructions on measuring
                            wavelengths and velocities based on emission
                            and absorption lines.

                            <div class="text-center mt-4">
                              <video-dialog
                                button-text="learn more"
                                title-text="How do we measure galaxy velocity?"
                                close-text="close"
                                @close="console.log('Close button was clicked.')"
                              >
                                Verbiage about comparing observed and
                                rest wavelengths of absorption/emission lines
                              </video-dialog>
                            </div>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-container>

                    <infodialog-alert>
                      This window provides a view of the "night sky". Left click and drag to pan around within the view. Roll your mouse wheel forward and backward to zoom in and out. (we can recycle instructions from the WWT interactives) <br>
                      The (colored) dots mark the locations of galaxies you can collect data for. Left click on one of these dots to select that galaxy. (is it going to be an issue if left click is "pan" and they accidentally click on one of the dots while trying to pan?) <br>
                    </infodialog-alert>
                    <infodialog-alert>
                      Notice that the table now has a row for your selected galaxy.
                    </infodialog-alert>
                    <infodialog-alert>
                      Great! Now let's take a look at your galaxy's spectrum. Recall that a spectrograph separates light from a source into its distinct colors. The spectrum graph shows how bright the light from the galaxy is at each color. Notice that the spectrum has one or more upward spiky lines that are very bright (emission lines) or downward dips that are faint (absorption lines). These lines are caused by specific atoms and molecules in the galaxy emitting or absorbing light at those particular colors. Look for one of the lines labeled as Hydrogen (H), Calcium (Ca), or Potassium (K).<br>
                    </infodialog-alert>
                    <infodialog-alert>
                      Left click on the vertical measuring tool and drag it to line up with the labeled line. Click again to record the observed wavelength of that line.
                    </infodialog-alert>
                    <infodialog-alert>
                      Notice your measurement is now recorded in the table.
                    </infodialog-alert>
                    <infodialog-alert>
                      Click on the H, Ca, or K label next to the line to record the rest wavelength of the line in the table.
                    </infodialog-alert>
                    <infodialog-alert>
                      Repeat this process for four more galaxies (or however many your instructor would like you to collect data for).
                    </infodialog-alert>

                    <!-- WIREFRAME for learning objectives/experience on First Page -->
                    <hinttext-alert>
                      This is for marginal hint text
                    </hinttext-alert>
                    <snackbar-alert>
                      This is for guidance snackbars
                    </snackbar-alert>
                    <infodialog-alert>
                      This is for informative dialog pop-ups
                    </infodialog-alert>
                    <responsedialog-alert>
                      This is for worksheet form pop-ups
                    </responsedialog-alert>
                  </v-stepper-content>
                  <!-- ---------------- --------------------------------- ---------------- -->
                  <!-- ---------------- SECOND PAGE: DISTANCE MEASUREMENT ---------------- -->
                  <!-- ---------------- --------------------------------- ---------------- -->
                  <v-stepper-content step="2">

                    <v-container>
                      <v-row>
                        <!-- This WWT viewer widget allows user to select a galaxy; galaxy positions plotted by RA/Dec.
                        It will zoom in to chosen galaxy & put controls/instructions on screen. -->
                        <!-- viewers.wwt_viewer doesn't need to be prepended with "state" because it comes from "Application" in app.py, not "ApplicationState"-->
                        <v-col cols="12" md="8">
                          <v-card>
                            <v-toolbar
                              color="pink"
                              dark
                            >
                              <v-icon left>
                                mdi-ruler
                              </v-icon>

                              <v-toolbar-title>Estimate Distance</v-toolbar-title>

                              <v-spacer></v-spacer>

                              <v-btn icon>
                                <v-icon>mdi-information-outline</v-icon>
                              </v-btn>
                            </v-toolbar>
                            <jupyter-widget
                              :widget="viewers.wwt_viewer"
                            ></jupyter-widget>
                          </v-card>
                        </v-col>

                        <!-- Callout to select galaxy / info about selected galaxy -->
                        <v-col cols="12" md="4">
                          <div
                            :class="state.haro_on"
                          >
                            <v-card
                              color="indigo lighten-5"
                              width="100%"
                            >
                              <v-card-title>Haro 11</v-card-title>
                              <v-card-text>
                                <v-divider></v-divider>
                                <v-list
                                  color="indigo lighten-5"
                                >
                                  <v-list-item-content>
                                    <v-list-item-title>Irregular galaxy</v-list-item-title>
                                    <v-list-item-subtitle>type</v-list-item-subtitle>
                                  </v-list-item-content>
                                  <v-list-item-content>
                                    <v-list-item-title>100,000 light years</v-list-item-title>
                                    <v-list-item-subtitle>assumed size</v-list-item-subtitle>
                                  </v-list-item-content>
                                  <v-list-item-content>
                                    <v-list-item-title>568 pixels</v-list-item-title>  
                                    <v-list-item-subtitle>height of display</v-list-item-subtitle>
                                  </v-list-item-content>
                                </v-list>
                                <v-divider></v-divider>
                                <v-text-field
                                  :value="state.galaxy_dist"
                                  label="Estimated Distance"
                                  hint="click button below"
                                  persistent-hint
                                  color="purple darken-2"
                                  class="mt-8 mb-4"
                                  suffix="Mpc"
                                  outlined
                                  readonly
                                  dense
                                ></v-text-field>
                                <v-btn
                                  block
                                  color="purple darken-2"
                                  dark
                                  class="px-auto"
                                  max-width="100%"
                                  @click="
                                    state.dist_measured = 1;
                                    state.gal_snackbar = 0;
                                    state.dist_snackbar = 0;
                                    state.marker_snackbar = 0;
                                    state.vel_snackbar = 0;
                                    state.data_ready_snackbar = 0;
                                    state.vel_measured == 1
                                      ? state.data_ready_snackbar = 1
                                      : state.dist_snackbar = 1;
                                    state.adddata_disabled =
                                      state.vel_measured == 1
                                        ? false
                                        : true;
                                    state.galaxy_dist = Math.floor(Math.random() * 450) + 50;
                                    add_distance_data_point();
                                  "
                                >
                                  estimate
                                </v-btn>
                              </v-card-text>
                            </v-card>
                          </div>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col
                          cols="3"
                        >
                          <v-alert
                            class="mb-4"
                            border="left"
                            colored-border
                            color="indigo"
                            elevation="2"
                          >
                            This will be text explaining how to use the distance measuring tool
                          </v-alert>
                          <v-btn
                            block
                            class="mb-4"
                            :disabled="state.adddata_disabled"
                            @click="state.next1_disabled = false"
                            color="primary"
                          >
                            <v-icon
                              left
                              dark
                            >
                              mdi-chart-scatter-plot
                            </v-icon>
                            graph data
                          </v-btn>
                        </v-col>
                        <v-col>
                          <c-distance-table/>
                          <todo-alert>
                            <ul>
                              <li>When students click on a row of the table to choose their galaxy, the WWT window will display that galaxy with the measurement tools (so this won't need to have both a "Select galaxy" and "Estimate Distance" tab. It can be consolidated to just an Estimate Distance header.)
                              <li>The button "graph data points" probably wants to take them straight to page 3, where the graph will be displayed.
                            </ul>
                          </todo-alert>
                        </v-col>
                      </v-row>
                    </v-container>

                    <!-- WIREFRAME for learning objectives/experience on First Page -->
                    <hinttext-alert>
                      This is for marginal hint text
                    </hinttext-alert>
                    <snackbar-alert>
                      This is for guidance snackbars
                    </snackbar-alert>
                    <infodialog-alert>
                      This is for informative dialog pop-ups
                    </infodialog-alert>
                    <responsedialog-alert>
                      This is for worksheet form pop-ups
                    </responsedialog-alert>
                  </v-stepper-content>

                <!-- This sets up the screen for the Analysis/data fitting step -->

                <!-- Will need buttons/functionality for:
                     * drawing by eye/calculating/plotting best fit lines
                     * Choosing different data sets - student/class/all
                     * Plotting by galaxy type -->

                  <!-- ---------------- ------------------------------------ ---------------- -->
                  <!-- ---------------- THIRD PAGE: ESTIMATE AGE OF UNIVERSE ---------------- -->
                  <!-- ---------------- ------------------------------------ ---------------- -->
                  <v-stepper-content step="3">
                    <v-container>
                      <v-row>
                        <v-col
                          cols="3"
                          class="align-stretch"
                        >
                          <div
                            class="d-flex mb-4"
                          >
                            <v-btn
                              :outlined="state.draw_on"
                              color="orange"
                              class="flex-grow-1 white--text"
                              @click="state.draw_on = !state.draw_on"
                            >
                              draw a fit line
                              <v-spacer></v-spacer>
                              <v-icon
                                right
                                dark
                                class="px-4"
                              >
                                mdi-draw
                              </v-icon>
                            </v-btn>
                          </div>
                          <div
                            class="d-flex mb-4"
                          >
                            <v-btn
                              color="green lighten-1"
                              class="flex-grow-1 white--text"
                              @click="fit_lines({
                                'viewer_id': 'hub_fit_viewer'
                                });
                                state.bestfit_on = 1"
                            >
                              find best fit
                              <v-spacer></v-spacer>
                              <v-icon
                                right
                                dark
                                class="px-4"
                              >
                                mdi-calculator
                              </v-icon>
                            </v-btn>
                          </div>
                        </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              :widget="viewers.hub_fit_viewer"
                            ></jupyter-widget>
                          </v-lazy>
                          <!-- TABLE to hold Galaxy, Velocity & Distance -->
                          <c-fit-table />
                        </v-col>
                      </v-row>
                      <v-row

                      >
                        <v-card
                          class="pa-8 mx-auto"
                        >
                          Watch this video for an explanation how and why we can calculate
                          the age of universe by inverting our <em>H</em><sub>0</sub> value.
                          <div class="text-center mt-4">
                            <video-dialog
                              button-text="learn more"
                              title-text="How do we estimate age of the universe?"
                              close-text="close"
                              @close="console.log('Close button was clicked.')"
                            >
                              Verbiage about how the slope of the Hubble plot is the inverse of the age of the universe.
                            </video-dialog>
                          </div>
                        </v-card>
                      </v-row>
                    </v-container>
                    
                    <!-- WIREFRAME for learning objectives/experience on First Page -->
                    <hinttext-alert>
                      This is for marginal hint text
                    </hinttext-alert>
                    <snackbar-alert>
                      This is for guidance snackbars
                    </snackbar-alert>
                    <infodialog-alert>
                      This is for informative dialog pop-ups
                    </infodialog-alert>
                    <responsedialog-alert>
                      This is for worksheet form pop-ups
                    </responsedialog-alert>
<!-- Disabling for now
                    <v-btn color="primary" @click="state.over_model = 3">
                      Continue
                    </v-btn>
                    <v-btn text> Cancel </v-btn>
-->
                  </v-stepper-content>

                <!-- This sets up the screen for the View Results step where they can look at distributions -->
                <!-- Will need buttons/functionality for choosing different data sets -->
                <!-- Need to think through whether the hubble plot should also appear on this page or if that would be confusing -->

                  <!-- ---------------- ------------------------------- ---------------- -->
                  <!-- ---------------- FOURTH PAGE: EXPLORE CLASS DATA ---------------- -->
                  <!-- ---------------- ------------------------------- ---------------- -->
                  <v-stepper-content step="4">
                    <v-container>
                      <v-row>
                        <v-col
                          cols="3"
                        ><v-btn
                            color="primary"
                            @click="fit_lines({
                              'viewer_id': 'hub_comparison_viewer'
                            })"
                          >
                            Fit Lines
                          </v-btn>
                          <v-list
                            style="max-height: 300px"
                            class="overflow-y-auto"
                          >
                            <v-list-item-group
                              multiple
                              v-model="state.hubble_comparison_selections"
                            >
                              <v-list-item
                                v-for="(option, index) in ['My data', 'Class data', 'All data']"
                                :key="index"
                                :value="index"
                              >
                                <template v-slot:default="{ active }">
                                  <v-list-item-content>
                                    {{option}}
                                  </v-list-item-content>

                                  <v-list-item-action>
                                    <v-checkbox
                                      :input-value="active"
                                      :color="['orange', 'green', 'red'][index]"
                                    ></v-checkbox>
                                  </v-list-item-action>
                                </template>
                              </v-list-item>
                            </v-list-item-group>
                          </v-list>
                        </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              :widget="viewers.hub_comparison_viewer"
                            ></jupyter-widget>
                          </v-lazy>
                          <todo-alert>
                            Give options to view all data from class, fit a
                            line, and calculate <em>H</em><sub>0</sub> and
                            age values for full class data set.
                          </todo-alert>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-card
                          class="pa-8"
                          elevation="3"
                          width="100%"
                        >

                          Buttons to calculate age of universe from H0 value.<br>

                          <help-dialog
                            button-text="Click Me!"
                            title-text="Testing!"
                            accept-text="Okay"
                            cancel-text="Cancel"
                            @accept="console.log('Button was clicked.')"
                          >
                            This is a test of a pure Vue dialog with a custom event.
                          </help-dialog>

                        </v-card>
                     </v-row>
                    </v-container>
                    
                    <!-- WIREFRAME for learning objectives/experience on First Page -->
                    <hinttext-alert>
                      This is for marginal hint text
                    </hinttext-alert>
                    <snackbar-alert>
                      This is for guidance snackbars
                    </snackbar-alert>
                    <infodialog-alert>
                      This is for informative dialog pop-ups
                    </infodialog-alert>
                    <responsedialog-alert>
                      This is for worksheet form pop-ups
                    </responsedialog-alert>

                  </v-stepper-content>

                  <!-- ---------------- ------------------------------ ---------------- -->
                  <!-- ---------------- FIFTH PAGE: VIEW DISTRIBUTIONS ---------------- -->
                  <!-- ---------------- ------------------------------ ---------------- -->
                  <v-stepper-content step="5">
                    <v-container>
                      <v-row>
                        <v-col cols="3">
                        </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              :widget="viewers.hub_students_viewer"
                            ></jupyter-widget>
                          </v-lazy>
                          <todo-alert>
                            Give options to look at galaxies &amp; distribution
                            of age values for individual students within class
                            or for unique classes within full data set.
                          </todo-alert>
                        </v-col>
                      </v-row>
                    </v-container>
                    <v-container>
                    <v-lazy>
                      <v-row>
                        <v-col>
                          <v-tabs>
                            <v-tab key="hist_class">My class</v-tab>
                            <v-tab key="hist_prob">All data</v-tab>
                            <v-tab key="hist_sandbox">Sandbox</v-tab>
                            <v-tab-item key="hist_class">
                              <v-container>
                                <v-row>
                                  <v-col cols="3">
                                    <v-list
                                      style="max-height: 300px"
                                      class="overflow-y-auto"
                                    >
                                      <v-list-item-group
                                        multiple
                                        v-model="state.class_histogram_selections"
                                      >
                                        <v-list-item
                                          v-for="(option, index) in ['Individual students', 'My value', 'Class value']"
                                          :key="index"
                                          :value="index"
                                        >
                                          <template v-slot:default="{ active }">
                                            <v-list-item-content>
                                              {{option}}
                                            </v-list-item-content>

                                            <v-list-item-action>
                                              <v-checkbox
                                                :input-value="active"
                                                :color="['orange', 'blue', 'green'][index]"
                                              ></v-checkbox>
                                            </v-list-item-action>
                                          </template>
                                        </v-list-item>
                                      </v-list-item-group>
                                    </v-list>
                                    <v-btn
                                      color="primary"
                                      @click="clear_histogram_selection()"
                                    >
                                    Clear selection
                                    </v-btn>
                                  </v-col>
                                  <v-col>
                                    <v-lazy>
                                      <jupyter-widget
                                        style="height: 300px"
                                        :widget="viewers.class_distr_viewer">
                                      </jupyter-widget>
                                    </v-lazy>
                                  </v-col>
                                </v-row>
                              </v-container>
                            </v-tab-item>
                            <v-tab-item key="hist_prob">
                              <v-container>
                                <v-row>
                                  <v-col cols="3">
                                    <v-list
                                      style="max-height: 300px"
                                      class="overflow-y-auto"
                                    >
                                      <v-list-item-group
                                        multiple
                                        v-model="state.alldata_histogram_selections"
                                      >
                                        <v-list-item
                                          v-for="(option, index) in ['Students','Classes']"
                                          :key="index"
                                          :value="index"
                                        >
                                          <template v-slot:default="{ active }">
                                            <v-list-item-content>
                                              {{option}}
                                            </v-list-item-content>

                                            <v-list-item-action>
                                              <v-checkbox
                                                :input-value="active"
                                                :color="['blue', 'red'][index]"
                                              ></v-checkbox>
                                            </v-list-item-action>
                                          </template>
                                        </v-list-item>
                                      </v-list-item-group>
                                    </v-list>
                                  </v-col>
                                  <v-col>
                                    <v-lazy>
                                      <jupyter-widget
                                        style="height: 300px"
                                        :widget="viewers.all_distr_viewer">
                                      </jupyter-widget>
                                    </v-lazy>
                                  </v-col>
                              </v-container>
                            </v-tab-item>
                            <v-tab-item key="hist_sandbox">
                              <v-container>
                                <v-row>
                                  <v-col cols="3">
                                    <v-list
                                      style="max-height: 300px"
                                      class="overflow-y-auto"
                                    >
                                      <v-list-item-group
                                        multiple
                                        v-model="state.sandbox_histogram_selections"
                                      >
                                        <v-list-item
                                          v-for="(option, index) in ['Students in my class', 'All students', 'All classes', 'My class', 'All data', 'My value']"
                                          :key="index"
                                          :value="index"
                                        >
                                          <template v-slot:default="{ active }">
                                            <v-list-item-content>
                                              {{option}}
                                            </v-list-item-content>

                                            <v-list-item-action>
                                              <v-checkbox
                                                :input-value="active"
                                                :color="['orange', 'blue', 'red', 'purple', 'green', 'black'][index]"
                                              ></v-checkbox>
                                            </v-list-item-action>
                                          </template>
                                        </v-list-item>
                                      </v-list-item-group>
                                    </v-list>
                                  </v-col>
                                  <v-col>
                                    <v-lazy>
                                      <jupyter-widget
                                        style="height: 300px"
                                        :widget="viewers.sandbox_distr_viewer">
                                      </jupyter-widget>
                                    </v-lazy>
                                  </v-col>
                              </v-container>
                            </v-tab-item>
                          </v-tabs>
                        </v-col>
                      </v-row>
                    </v-lazy>
                    <v-card
                      class="fill-height mb-12"
                      color="grey lighten-1 elevation-0"
                    ></v-card>
                    <v-card
                      class="fill-height mb-12"
                      color="grey lighten-1 elevation-0"
                    ></v-card>
                    
                    <!-- WIREFRAME for learning objectives/experience on First Page -->
                    <hinttext-alert>
                      This is for marginal hint text
                    </hinttext-alert>
                    <snackbar-alert>
                      This is for guidance snackbars
                    </snackbar-alert>
                    <infodialog-alert>
                      This is for informative dialog pop-ups
                    </infodialog-alert>
                    <responsedialog-alert>
                      This is for worksheet form pop-ups
                    </responsedialog-alert>
                    
<!-- disabling this because it's redundant with previous/next
                    <v-btn color="primary" @click="state.over_model = 1">
                      Continue
                    </v-btn>
                    <v-btn text> Cancel </v-btn>
-->
                  <!-- Curly braces indicate text to be replaced by content in the variable,
                  like {{state.dialog_text}}  (For example, in app.py file, you can collect
                  student userID and display it here via something like "Hello <student userID>".) -->
                  </v-stepper-content>

                  <!-- ---------------- ----------------------------- ---------------- -->
                  <!-- ---------------- SIXTH PAGE: GALAXY MORPHOLOGY ---------------- -->
                  <!-- ---------------- ----------------------------- ---------------- -->
                  <v-stepper-content step="6">
                    <v-container>
                      <v-row>
                        <v-col
                          cols="3"
                        ><v-btn
                            color="primary"
                            @click="fit_lines({
                              'viewer_id': 'hub_morphology_viewer'
                            })"
                          >
                            Fit Lines
                          </v-btn>
                          <v-list
                            style="max-height: 300px"
                            class="overflow-y-auto"
                          >
                            <v-list-item-group
                              multiple
                              v-model="state.morphology_selections"
                            >
                              <v-list-item
                                v-for="(option, index) in ['Elliptical', 'Spiral', 'Irregular']"
                                :key="index"
                                :value="index"
                              >
                                <template v-slot:default="{ active }">
                                  <v-list-item-content>
                                    {{option}}
                                  </v-list-item-content>

                                  <v-list-item-action>
                                    <v-checkbox
                                      :input-value="active"
                                      :color="['orange', 'green', 'red'][index]"
                                    ></v-checkbox>
                                  </v-list-item-action>
                                </template>
                              </v-list-item>
                            </v-list-item-group>
                          </v-list>
                        </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              :widget="viewers.hub_morphology_viewer"
                            ></jupyter-widget>
                          </v-lazy>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-card
                          class="pa-8"
                          elevation="3"
                          width="100%"
                        >

                          Buttons to calculate age of universe from H0 value.<br>

                          <help-dialog
                            button-text="Click Me!"
                            title-text="Testing!"
                            accept-text="Okay"
                            cancel-text="Cancel"
                            @accept="console.log('Button was clicked.')"
                          >
                            This is a test of a pure Vue dialog with a custom event.
                          </help-dialog>

                        </v-card>
                     </v-row>
                    </v-container>

                    <!-- WIREFRAME for learning objectives/experience on First Page -->
                    <hinttext-alert>
                      This is for marginal hint text
                    </hinttext-alert>
                    <snackbar-alert>
                      This is for guidance snackbars
                    </snackbar-alert>
                    <infodialog-alert>
                      This is for informative dialog pop-ups
                    </infodialog-alert>
                    <responsedialog-alert>
                      This is for worksheet form pop-ups
                    </responsedialog-alert>

                  </v-stepper-content>



                  <!-- ---------------- -------------------------------- ---------------- -->
                  <!-- ---------------- SEVENTH PAGE: PRO ASTRONOMY DATA ---------------- -->
                  <!-- ---------------- -------------------------------- ---------------- -->

                  <v-stepper-content step="7">
                    <v-container>
                      <v-row>
                        <v-col
                          cols="3"
                        ><v-btn
                            color="primary"
                            @click="fit_lines({
                              'viewer_id': 'hub_comparison_viewer'
                            })"
                          >
                            Fit Lines
                          </v-btn>
                          <v-list
                            style="max-height: 300px"
                            class="overflow-y-auto"
                          >
                            <v-list-item-group
                              multiple
                              v-model="state.hubble_comparison_selections"
                            >
                            <!--
                              <v-list-item
                                v-for="(option, index) in ['My data', 'Class data', 'All data']"
                                :key="index"
                                :value="index"
                              >
                              -->
                              <v-list-item
                                v-for="(option, index) in ['Hubble (1929)', 'HST Key Project (2001)', 'Supernova Ia (2004)']"
                                :key="index"
                                :value="index"
                              >
                                <template v-slot:default="{ active }">
                                  <v-list-item-content>
                                    {{option}}
                                  </v-list-item-content>

                                  <v-list-item-action>
                                    <v-checkbox
                                      :input-value="active"
                                      :color="['orange', 'green', 'red'][index]"
                                    ></v-checkbox>
                                  </v-list-item-action>
                                </template>
                              </v-list-item>
                            </v-list-item-group>
                          </v-list>
                        </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              :widget="viewers.hub_comparison_viewer"
                            ></jupyter-widget>
                          </v-lazy>
                          <todo-alert>
                            Right now the check boxes are still tied to "My data", "Class data", and "All data". Need to replace those with links to the real scientific data.
                          </todo-alert>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-card
                          class="pa-8"
                          elevation="3"
                          width="100%"
                        >

                          Buttons to calculate age of universe from H0 value.<br>

                          <help-dialog
                            button-text="Click Me!"
                            title-text="Testing!"
                            accept-text="Okay"
                            cancel-text="Cancel"
                            @accept="console.log('Button was clicked.')"
                          >
                            This is a test of a pure Vue dialog with a custom event.
                          </help-dialog>

                        </v-card>
                     </v-row>
                    </v-container>

                    <!-- WIREFRAME for learning objectives/experience on First Page -->
                    <hinttext-alert>
                      This is for marginal hint text
                    </hinttext-alert>
                    <snackbar-alert>
                      This is for guidance snackbars
                    </snackbar-alert>
                    <infodialog-alert>
                      This is for informative dialog pop-ups
                    </infodialog-alert>
                    <responsedialog-alert>
                      This is for worksheet form pop-ups
                    </responsedialog-alert>

                  </v-stepper-content>

                </v-stepper-items>
              </v-stepper>
              <v-spacer></v-spacer>
              <v-divider></v-divider>
              <v-card-actions>
                <v-btn
                  :disabled="state.over_model == 1 ? true : false"
                  color="primary"
                  @click="
                    state.over_model =
                      state.over_model > 1
                        ? state.over_model - 1
                        : state.over_model
                  "
                >
                  Previous
                </v-btn>
                <v-spacer></v-spacer>

                <!-- for TESTING, use the following -- :disabled="false" -->
                <!-- for FINAL, use the following -- :disabled="state.over_model == 4 ? true : state.next1_disabled" -->
                <v-btn
                  :disabled="false"
                  color="primary"
                  dark
                  @click="
                    state.over_model =
                      state.over_model < 7
                        ? state.over_model + 1
                        : state.over_model
                  "
                >
                  {{ state.over_model == 7 ? 'Finish' : 'Next' }}
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
        <c-footer />
      </v-container>
    </v-main>

    <v-snackbar
      v-model="state.gal_snackbar"
      style="position: absolute"
      color="green"
    >
      Galaxy selected.
      <v-btn
        dark
        text
        @click="
          state.gal_snackbar = 0;
        "
      >
          Close
      </v-btn>
    </v-snackbar>

    <v-snackbar
      v-model="state.dist_snackbar"
      style="position: absolute"
      color="green"
    >
      Distance measured.
      <v-btn
        dark
        text
        @click="
          state.dist_snackbar = 0;
          state.col_tab_model = 1
        "
      >
          Go to Measure Velocity
      </v-btn>
    </v-snackbar>

    <v-snackbar
      v-model="state.marker_snackbar"
      style="position: absolute"
      color="green"
    >
      Wavelength marker set.
      <v-btn
        dark
        text
        @click="
          state.marker_snackbar = 0;
        "
      >
          Close
      </v-btn>
    </v-snackbar>

    <v-snackbar
      v-model="state.vel_snackbar"
      style="position: absolute"
      color="green"
    >
      Velocity measured.
      <v-btn
        dark
        text
        @click="
          state.vel_snackbar = 0;
          state.col_tab_model = 0
        "
      >
          Go to Estimate Distance
      </v-btn>
    </v-snackbar>

    <v-snackbar
      v-model="state.data_ready_snackbar"
      style="position: absolute"
      color="primary"
    >
      Great! You've estimated both distance and velocity for your galaxy.
      Now you can add these measurements to your dataset.
      <v-btn
        text
        @click="
          state.data_ready_snackbar = 0;
        "
        icon
        large
        dark
      >
          <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-snackbar>
  </v-app>  
</template>

<style id="cosmicds-app">
html {
  margin: 0;
  padding: 0;
}
body {
  margin: 0;
  padding: 0;
}
.jupyter-widgets .jp-Cell .jp-CodeCell .jp-Notebook-cell .jp-mod-noInput {
  margin: 0;
  padding: 0;
}
#cosmicds-app {
  height: 100%;
}
#app {
  height: 100vh;
}
.card-outter {
  position: relative;
  padding-bottom: 50px;
}
.card-actions {
  position: absolute;
  bottom: 0;
}
.v-stepper__wrapper {
  height: 100%;
}
.bqplot {
  height: 100%;
}
.v-stepper__content {
  min-height: 500px;
}
.v-tabs-items {
  min-height: 300px;
}

.no-transition .v-stepper__content {
  transition: none !important;
}
</style>
