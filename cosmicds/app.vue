<template>
  <v-app id="cosmicds-app">
    <v-app-bar
      color="primary"
      dark
      src="https://cdn.eso.org/images/screen/eso1738b.jpg"
      scroll-target="#scrolling-techniques-4"
    >
      <template v-slot:img="{ props }">
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
    This is a test
    <v-main id="scrolling-techniques-4" class="overflow-y-auto fill-height">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" xl="8">
            <v-card class="d-flex flex-column">

            <!-- This sets up the 3 step sections across the top -->
            <!-- v-model is a 2-way token that controls the state of something in the app-->
              <v-stepper v-model="state.over_model" class="elevation-0">
                <v-stepper-header>
                  <!--:complete="state.over_model > 1"
                        : is a binding - binds state of "complete" to the thing in the "".  If over_model is > 1, then we have gone past step 1.
                  therefore, consider step 1 complete. -->
                  <!-- Another example could be something like :disabled = "state.continue_button_disabled=1"-->
                  <v-stepper-step
                    :complete="state.over_model > 1"
                    step="1"
                    editable
                  >
                    Collect Galaxy Data
                  </v-stepper-step>

                  <v-divider></v-divider>

                  <v-stepper-step
                    :complete="state.over_model > 2"
                    step="2"
                    editable
                  >
                    Estimate Age of Universe
                  </v-stepper-step>

                  <v-divider></v-divider>

                  <v-stepper-step
                    :complete="state.over_model > 3"
                    step="3"
                    editable
                    >Explore Class Data
                  </v-stepper-step>


                  <v-divider></v-divider>

                  <v-stepper-step
                    :complete="state.over_model > 4"
                    step="4"
                    editable
                    >View Distributions
                  </v-stepper-step>
                </v-stepper-header>
              <!-- This sets up the screen for the galaxy selection/measurement step -->
                <v-stepper-items
                  class=""
                >
                  <!-- --- ---------- --- -->
                  <!-- --- FIRST PAGE --- -->
                  <!-- --- ---------- --- -->
                  <v-stepper-content step="1">
                    <v-container>
                      <v-row>
                        <v-col
                          cols="3"
                        ><v-alert
                            class="pa-5"
                            height="100%"
                            border="left"
                            colored-border
                            color="indigo"
                            elevation="3"
                          >
                            Velocity and distance measurements students add will be plotted here. (No data displayed to start. Points are added to plot as students measure and submit them.)
                          </v-alert>
                        </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              :widget="viewers.hub_const_viewer"
                            ></jupyter-widget>
                          </v-lazy>
                        </v-col>
                      </v-row>
                    </v-container>
                    <v-card
                      color="blue lighten-5"
                      class=""
                      outlined
                    >
                      <v-tabs
                        vertical
                        v-model="state.col_tab_model"
                      >
                        <v-tab key="gal-dist"> Estimate Distance </v-tab>
                        <v-tab key="gal-vel"> Measure Velocity </v-tab>
                        <v-tab-item key="gal-dist">
                          <v-container>
                            <v-row>
                              <!-- This WWT viewer widget allows user to select a galaxy; galaxy positions plotted by RA/Dec.
                              It will zoom in to chosen galaxy & put controls/instructions on screen. -->
                              <!-- viewers.wwt_viewer doesn't need to be prepended with "state" because it comes from "Application" in app.py, not "ApplicationState"-->
                              <v-col cols="12" md="8">
                                <jupyter-widget
                                  :widget="viewers.wwt_viewer"
                                ></jupyter-widget>
                              </v-col>

                              <!-- Callout to select galaxy / info about selected galaxy -->
                              <v-col cols="12" md="4">
                                <v-alert
                                  class="mb-12"
                                  border="left"
                                  colored-border
                                  color="indigo"
                                  elevation="2"
                                >
                                  Pan the sky and select one of the galaxies
                                  to measure.
                                  <div class="text-center mt-4">
                                    <v-btn
                                      class="white--text"
                                      color="purple darken-2"
                                      @click="
                                        state.gal_snackbar = 1;
                                        state.gal_selected = 1;
                                        state.haro_on = 'd-block'
                                      "
                                    >
                                      Select Galaxy
                                    </v-btn>
                                  </div>
                                </v-alert>
                                <div
                                  :class="state.haro_on"
                                >
                                  <v-card
                                    v-model="state.haro_on"
                                    color="indigo lighten-5"
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
                                          state.vel_measured == 1
                                            ? state.data_ready_snackbar = 1
                                            : state.dist_snackbar = 1;
                                          state.adddata_disabled =
                                            state.vel_measured == 1
                                              ? false
                                              : true;
                                          state.galaxy_dist = Math.floor(Math.random() * 450) + 50
                                        "
                                      >
                                        estimate
                                      </v-btn>
                                    </v-card-text>
                                  </v-card>
                                </div>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-tab-item>

                        <v-tab-item key="gal-vel">
                          <v-container>
                            <v-row>
                              <v-col
                                cols="12" md="7"
                                class="align-stretch"
                              >
                                <v-card
                                  min-height="300px"
                                  class="pa-5"
                                >
                                  TO DO: learn how to import
                                  Spectrum Lab .js code here.
                                </v-card>
                              </v-col>
                              <v-col cols="12" md="5">
                                <v-alert
                                  border="left"
                                  colored-border
                                  color="indigo"
                                  elevation="2"
                                  clas="mb-4"
                                >
                                  Drag across the spectrum to
                                  measure the H-&#x3B1; wavelength.
                                </v-alert>

                                <v-btn
                                  block
                                  class="white--text mb-12"
                                  color="purple darken-2"
                                  @click="

                                    state.vel_measured = 1;
                                    state.dist_measured == 1
                                      ? state.data_ready_snackbar = 1
                                      : state.vel_snackbar = 1;
                                    state.adddata_disabled =
                                      state.dist_measured == 1
                                        ? false
                                        : true
                                  "
                                >
                                  Calculate Velocity
                                </v-btn>
                                <v-card
                                  outlined
                                  class="pa-5"
                                  color="amber lighten-5"
                                  elevation="0"
                                >
                                  Instructions for measuring
                                  emission/absorption line wavelength and velocity.
                                  <div class="text-center mt-4">
                                    <c-dialog-vel class="mt-4"></c-dialog-vel>
                                  </div>
                                </v-card>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-tab-item>
                    </v-card>

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

                  <!-- --- ----------- --- -->
                  <!-- --- SECOND PAGE --- -->
                  <!-- --- ----------- --- -->
                  <v-stepper-content step="2">
                    <v-container>
                      <v-row>
                        <v-col
                          cols="3"
                          class="align-stretch"
                        >
                          <v-btn
                            @click="fit_lines({
                              'viewer_id': 'hub_fit_viewer'
                              })"
                            color="primary"
                          >
                          Fit Line
                          </v-btn>
                        </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              :widget="viewers.hub_fit_viewer"
                            ></jupyter-widget>
                          </v-lazy>
                        </v-col>
                      </v-row>
                      <v-row

                      >
                        <v-card
                          class="pa-8 mx-auto"
                        >
                          Buttons to call up explanation of why inverting H0 gives you
                          the age of the universe and to calculate age of universe from H0 value.
                          <div class="text-center mt-4">
                            <c-dialog-age></c-dialog-age>
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

                  <!-- --- ---------- --- -->
                  <!-- --- THIRD PAGE --- -->
                  <!-- --- ---------- --- -->
                  <v-stepper-content step="3">
                    <v-container>
                      <v-row>
                        <v-col
                          cols="3"
                        ><v-alert
                            class="pa-5"
                            height="300px"
                            border="left"
                            colored-border
                            color="indigo"
                            elevation="3"
                          >
                            Now give options to view all data from class, fit a
                            line, and calculate H0/age values for full class data set.
                          </v-alert>
                        </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              :widget="viewers.hub_const_viewer"
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

                  <!-- --- ----------- --- -->
                  <!-- --- FOURTH PAGE --- -->
                  <!-- --- ----------- --- -->
                  <v-stepper-content step="4">
                    <v-container>
                      <v-row>
                        <v-col
                          cols="3"
                        ><v-alert
                            class="pa-5"
                            height="100%"
                            border="left"
                            colored-border
                            color="indigo"
                            elevation="3"
                          >
                            Give options to look at galaxies &amp; distribution of age values for
                            individual students within class or for unique classes within full data set.
                          </v-alert>
                        </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              :widget="viewers.hub_const_viewer"
                            ></jupyter-widget>
                          </v-lazy>
                        </v-col>
                      </v-row>
                    </v-container>
                    <v-container>
                    <v-lazy>
                      <v-row>
                          <v-col cols="3">
                            <v-alert
                              class="pa-5"
                              height="100%"
                              border="left"
                              colored-border
                              color="indigo"
                              elevation="3"
                            >
                              Regular histogram to start. Give option to turn into stacked histogram
                              with legend that provides option to select specific students or classes
                              and highlight in top plot galaxies used to get that age estimate.
                            </v-alert>
                          </v-col>
                          <v-col>
                            <v-lazy>
                              <jupyter-widget
                                style="height: 300px"
                                :widget="viewers.age_distr_viewer">
                              </jupyter-widget>
                            </v-lazy>
                          </v-col>

                      </v-row>
                    </v-container
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

                </v-stepper-items>
              </v-stepper>
              <v-spacer></v-spacer>
              <v-divider></v-divider>
              <v-card-actions>
                <!-- Turning this off for now since it doesn't do anything yet.
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

                <v-btn
                  :disabled="state.adddata_disabled"
                  @click="state.next1_disabled = false"
                >
                  <v-icon
                    left
                    dark
                  >
                    mdi-plus
                  </v-icon>
                  Add Data
                </v-btn>
                <!-- for TESTING, use the following -- :disabled="false" -->
                <!-- for FINAL, use the following -- :disabled="state.over_model == 4 ? true : state.next1_disabled" -->
                <v-btn
                  :disabled="false"
                  color="primary"
                  @click="
                    state.over_model =
                      state.over_model < 4
                        ? state.over_model + 1
                        : state.over_model
                  "
                >
                  {{ state.over_model == 4 ? 'Finish' : 'Next' }}
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
      color="green"
    >
      Great! You've estimated both distance and velocity for your galaxy. Now you can add these measurements to your dataset.
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
</style>
