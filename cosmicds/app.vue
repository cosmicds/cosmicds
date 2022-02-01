<template>
  <v-app
    id="cosmicds-app"
  >
    <!-- TOOLBAR, fixed to the top of the application -->
    <v-app-bar
      color="primary"
      dark
      src="https://cdn.eso.org/images/screen/eso1738b.jpg"
      scroll-target="#scrolling-techniques-4"
    >
      <!-- Sets the BACKGROUND IMAGE and GRADIENT overlay -- original RGBA values: "to top right, rgba(100,115,201,.7), rgba(25,32,72,.7)" -->
      <template
        v-slot:img="{ props }"
      >
        <v-img
          v-bind="props"
          gradient="to top right, rgba(1, 87, 155, .7), rgba(0, 0, 0, .5)"
        ></v-img>
      </template>

      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <v-toolbar-title>
        Hubble's Law
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn
        icon
        @click="
          toggle_darkmode()
          state.darkmode = !state.darkmode
        "
      >
        <v-icon
        >mdi-white-balance-sunny</v-icon>
      </v-btn>

      <v-btn
        icon
        @click="
          state.marker = 'sel_gal1';
          state.toggle_on = 'd-none';
          state.toggle_off = 'd-block';
          state.gal_selected = 0;
          state.spectrum_tool_visible = 0;
          state.waveline_set = 0;
        "
      >
        <v-icon
        >mdi-replay</v-icon>
      </v-btn>

      <v-btn
        icon
        @click="
          state.marker = 'nic_wor1';
          state.toggle_on = 'd-block';
          state.toggle_off = 'd-none';
          state.gal_selected = 1;
          state.spectrum_tool_visible = 1;
          add_galaxy_data_point();
          add_galaxy_data_point();
          add_galaxy_data_point();
          add_galaxy_data_point();
          add_galaxy_data_point();
          state.gals_total += 5;
          state.waveline_set = 0;
        "
      >
        <v-icon
          :class="state.toggle_off"
        >mdi-toggle-switch-off-outline</v-icon>
        <v-icon
          :class="state.toggle_on"
        >mdi-toggle-switch</v-icon>
      </v-btn>
      <v-toolbar-title>
        Cosmic Data Stories
      </v-toolbar-title>
      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>

    </v-app-bar>

    <!-- The MAIN section of the application -->
    <v-main
      id="scrolling-techniques-4"
      class="overflow-y-auto fill-height"
    >
      <v-container
        class="py-0"
      >
        <v-row justify="center">
          <v-col cols="12" xl="8">
            <v-row justify="center">
              <v-col cols="2">
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
                  tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                  quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
                </p>
              </v-col>
              <v-col cols="10">
                <v-card
                  class="d-flex flex-column"
                >

                <!-- The STEPPER that sets up the multi-step sections across the top -->
                <!-- Note: V-MODEL is a 2-way token that controls the state of something in the app -->
                  <v-stepper
                    v-model="state.over_model"
                    class="elevation-0"
                  >
                    <!-- Navigational banner for each of the STEPPER STEPS -->
                    <v-stepper-header
                      dense
                    >
                      <v-stepper-step
                        :complete="state.over_model > 1"
                        step="1"
                        editable
                      >
                        Collect Velocity Data
                      </v-stepper-step>

                      <v-divider></v-divider>

                      <v-stepper-step
                        :complete="state.over_model > 2"
                        step="2"
                        editable
                      >
                        Collect Distance Data
                      </v-stepper-step>

                      <v-divider></v-divider>

                      <v-stepper-step
                        :complete="state.over_model > 3"
                        step="3"
                        editable
                      >
                        Explore Data
                      </v-stepper-step>
                    </v-stepper-header>

                    <!-- STEPPER-ITEMS to hold all content of each STEPPER -->
                    <v-stepper-items
                      class=""
                    >

                      <!-- ---------------- -------------------------------- ---------------- -->
                      <!-- ---------------- -------------------------------- ---------------- -->
                      <!-- ---------------- FIRST PAGE: VELOCITY MEASUREMENT ---------------- -->
                      <!-- ---------------- -------------------------------- ---------------- -->
                      <!-- ---------------- -------------------------------- ---------------- -->
                      <v-stepper-content step="1">
                        <v-container
                          class="pt-0"
                        >
                          <v-row>
                            <v-col
                              cols="6"
                              class="wwt_column"
                            >
                              <!-- The CARD to hold the WWT VIEWER and where students Select Galaxies -->
                              <v-card
                                
                                :color="state.marker == 'sel_gal1' ? 'info' : 'none'"
                                :class="state.marker == 'sel_gal1' ? 'pa-1' : 'pa-0'"
                              >
                                <v-toolbar
                                  color="secondary"
                                  dense
                                  dark
                                >
                                  <v-toolbar-title>Night Sky Viewer</v-toolbar-title>

                                  <v-spacer></v-spacer>

                                  <v-btn icon>
                                    <v-icon>mdi-information-outline</v-icon>
                                  </v-btn>
                                </v-toolbar>
                                <!-- WIDGET for WWT galaxy selection -->
                                <div
                                  class="wwt_widget"
                                >
                                  <!-- WWT GALAXY PICKER as Jupyter Widget -- v-lazy loads when visible -->
                                  <v-lazy>
                                    <jupyter-widget
                                      :widget="viewers.wwt_viewer"
                                    ></jupyter-widget>
                                  </v-lazy>
                                </div>
                              </v-card>
                            </v-col>
                            <v-col
                              cols="6"
                              class="galtable_column"
                            >
                              <!-- The CARD to hold the WWT VIEWER and where students Select Galaxies -->
                              <v-card
                                
                                :color="state.marker == 'cho_row1' ? 'info' : 'none'"
                                :class="state.marker == 'cho_row1' ? 'pa-1' : 'pa-0'"
                              >
                                <!-- TABLE to hold Selected Galaxies -->
                                <c-galaxy-table />
                              </v-card>
                            </v-col>
                          </v-row>
                          <v-row
                            :class="state.marker == 'sel_gal1' | state.marker == 'cho_row1' ? 'd-block' : 'd-none'"
                          >
                            <v-col>

                              <!-- GUIDANCE ALERT - Show students how to select galaxies -->
                              <v-alert
                                :class="state.marker == 'sel_gal1' ? 'd-block' : 'd-none'"
                                color="info"
                                class="mb-4"
                                elevation="6"
                              >
                                <h3
                                  class="mb-4"
                                >
                                  Select Five Galaxies
                                </h3>
                                <div
                                  :class="state.gals_total == 0 ? 'd-block' : 'd-none'"
                                  class="mb-4"
                                >
                                  <p>
                                    This is another view of the night sky, similar to the one you explored earlier. This view shows a more modern data set from the Sloan Digital Sky Survey (SDSS), which has collected imaging and spectral data for millions of galaxies. This Data Story will focus on a nearby subset of galaxies.
                                  </p>
                                  <p>
                                    The <strong :class="state.darkmode ? 'green--text text--lighten-3' : 'green--text text--darken-2'">green</strong> dots mark the locations of galaxies you can collect data for. 
                                  </p>
                                  <p>
                                    Pan around the sky and click on one of these dots to select that galaxy.
                                  </p>
                                </div>
                                <div
                                  :class="state.gals_total == 1 ? 'd-block' : 'd-none'"
                                  class="mb-4"
                                >
                                  <p>
                                    Notice that the table now has a row for your selected galaxy.
                                  </p>
                                  <p>
                                    Now pan around the sky and choose a different galaxy to enter into your table.
                                  </p>
                                </div>
                                <div
                                  :class="state.gals_total > 1 & state.gals_total < 5 ? 'd-block' : 'd-none'"
                                  class="mb-4"
                                >
                                  <p>
                                    Check it out, your table is growing.
                                  </p>
                                  <p>
                                    Keep selecting random galaxies until you have 5 rows in your table.
                                  </p>
                                </div>
                                <div
                                  :class="state.gals_total == 5 ? 'd-block' : 'd-none'"
                                  class="mb-4"
                                >
                                  <p>
                                    Great, you've got all the galaxies that you need in order to start.
                                  </p>
                                  <p>
                                    Now you can start making measurements from your data.
                                  </p>
                                </div>
                                <div
                                  class="text-center my-8"
                                >
                                  <v-btn
                                    class="black--text"
                                    color="success"
                                    elevation="2"
                                    :disabled="state.gals_total == 5"
                                    @click="
                                      state.gal_snackbar = 0;
                                      state.dist_snackbar = 0;
                                      state.marker_snackbar = 0;
                                      state.vel_snackbar = 0;
                                      state.data_ready_snackbar = 0;
                                      state.gal_snackbar = 1;
                                      state.gal_selected = 1;
                                      state.gals_total += 1;
                                      add_galaxy_data_point();
                                    "
                                  >
                                    select galaxy
                                  </v-btn>
                                </div>
                                <div
                                  class="mb-2 mx-4"
                                >
                                  <v-row
                                    no-gutters
                                    class="mb-3"
                                  >
                                    <v-col
                                      cols="3"
                                    >
                                      <strong>Pan</strong>
                                    </v-col>
                                    <v-col
                                      cols="9"
                                    >
                                      <strong>click + drag</strong><br>
                                      (or use the <strong class="codeFont">I-J-K-L</strong> keys)
                                    </v-col>
                                  </v-row>
                                  <v-row
                                    no-gutters
                                  >
                                    <v-col
                                      cols="3"
                                    >
                                      <strong>Zoom</strong>
                                    </v-col>
                                    <v-col
                                      cols="9"
                                    >
                                      <strong>scroll in and out</strong><br>
                                      (or use the <strong class="codeFont">Z-X</strong> keys for finer zoom)
                                    </v-col>
                                  </v-row>
                                </div>
                                
                                <v-divider
                                  class="my-4"
                                >
                                </v-divider>

                                <v-row
                                  align="center"
                                  no-gutters
                                >
                                  <v-spacer></v-spacer>
                                  
                                  <v-col
                                    cols="3"
                                    class="shrink"
                                    :class="state.gals_total < 5 ? 'd-block' : 'd-none'"
                                  >
                                    <div
                                    >
                                      Select {{ 5 - state.gals_total }} more <span :class="state.gals_total < 4 ? 'd-inline' : 'd-none'">galaxies</span><span :class="state.gals_total == 4 ? 'd-inline' : 'd-none'">galaxy</span> before moving on.
                                    </div>
                                  </v-col>
                                  <v-col
                                    class="shrink"
                                    :class="state.gals_total == 5 ? 'd-block' : 'd-none'"
                                  >
                                    <v-btn
                                      class="black--text"
                                      color="accent"
                                      elevation="2"
                                      @click="
                                        state.marker = 'cho_row1';
                                      "
                                    >
                                      next
                                    </v-btn>
                                  </v-col>
                                </v-row>
                              </v-alert>

                              <!-- GUIDANCE ALERT - Request specific galaxy to work with -->
                              <v-alert
                                :class="state.marker == 'cho_row1' ? 'd-block' : 'd-none'"
                                color="info"
                                class="mb-4"
                                elevation="6"
                              >
                                <h3
                                  class="mb-4"
                                >
                                  Choose a Row
                                </h3>
                                <div
                                  class="mb-4"
                                >
                                  <p>
                                    Let's take a look at the light spectrum for one of your galaxies.
                                  </p>
                                  <p>
                                    Click on a row in your table to choose that galaxy.
                                  </p>
                                </div>
                                <v-divider
                                  class="my-4"
                                >
                                </v-divider>

                                <v-row
                                  align="center"
                                  no-gutters
                                >
                                  <v-col>
                                    <v-btn
                                      class="black--text"
                                      color="accent"
                                      elevation="2"
                                      @click="
                                        state.marker = 'sel_gal1';
                                      "
                                    >
                                      back
                                    </v-btn>
                                  </v-col>
                                  <v-spacer></v-spacer>
                                  <v-col
                                    class="shrink"
                                  >
                                    <v-btn
                                      class="black--text"
                                      color="accent"
                                      elevation="2"
                                      @click="
                                        state.spectrum_tool_visible = 1;
                                        state.marker = 'mee_spe1';
                                      "
                                    >
                                      next
                                    </v-btn>
                                  </v-col>
                                </v-row>
                              </v-alert>
                            </v-col>
                          </v-row>
                        </v-container>
                        <v-container
                          :class="state.spectrum_tool_visible ? 'd-block' : 'd-none'"
                          class="py-0"
                        >
                          <v-row>
                            <v-col
                              cols="12" md="8"
                              class="align-stretch"
                            >
                              <!-- The CARD to hold the SPECTRUM TOOL and where students Measure Velocity -->
                              <v-card
                                :class="state.spectrum_tool_visible ? 'd-block' : 'd-none'"
                                min-height="300px"
                                outlined
                                color="info"
                                class="pa-1"
                              >
                                <v-toolbar
                                  color="secondary"
                                  dense
                                  dark
                                >
                                  <v-toolbar-title>Spectrum Tool</v-toolbar-title>

                                  <v-spacer></v-spacer>

                                  <v-btn icon>
                                    <v-icon>mdi-information-outline</v-icon>
                                  </v-btn>
                                </v-toolbar>
                                  <v-lazy>
                                    <jupyter-widget :widget="viewers.spectrum_viewer" >
                                    </jupyter-widget>  
                                  </v-lazy>
                              </v-card>
                            </v-col>
                            <!-- SIDEBAR COLUMN for processing velocity data -->
                            <v-col cols="12" md="4">

                              <!-- GUIDANCE ALERT - Spectrum Tool #1 -->
                              <v-alert
                                :class="state.marker == 'mee_spe1' ? 'd-block' : 'd-none'"
                                class="mb-4"
                                color="info"
                                elevation="6"
                              >
                                <h3
                                  class="mb-4"
                                >
                                  Meet the Spectrum Tool
                                </h3>
                                <div
                                  class="mb-4"
                                >
                                  <p>
                                    To the left is a spectrum of light from your chosen galaxy.
                                  </p>
                                  <p>
                                    Let’s learn how a spectrum can tell us if an object is moving toward or away from us.
                                  </p>
                                </div>
                                <v-divider
                                  class="my-4"
                                >
                                </v-divider>

                                <v-row
                                  align="center"
                                  no-gutters
                                >
                                  <v-col>
                                    <v-btn
                                      class="black--text"
                                      color="accent"
                                      elevation="2"
                                      @click="
                                        state.marker = 'cho_row1';
                                        state.spectrum_tool_visible = 0;
                                      "
                                    >
                                      back
                                    </v-btn>
                                  </v-col>
                                  <v-spacer></v-spacer>
                                  
                                  <v-col
                                    cols="6"
                                    class="shrink"
                                    :class="state.vel_win_unopened ? 'd-block' : 'd-none'"
                                  >
                                    <div
                                    >
                                      Click INFO below.
                                    </div>
                                  </v-col>
                                  <v-col
                                    class="shrink"
                                    :class="state.vel_win_unopened ? 'd-none' : 'd-block'"
                                  >
                                    <v-btn
                                      class="black--text"
                                      color="accent"
                                      elevation="2"
                                      @click="
                                        state.marker = 'res_wav1';
                                      "
                                    >
                                      next
                                    </v-btn>
                                  </v-col>
                                </v-row>
                              </v-alert>

                              <!-- GUIDANCE ALERT - Spectrum Tool #2 -->
                              <v-alert
                                :class="state.marker == 'res_wav1' ? 'd-block' : 'd-none'"
                                class="mb-4"
                                color="info"
                                elevation="6"
                              >
                                <h3
                                  class="mb-4"
                                >
                                  Rest Wavelength
                                </h3>
                                <div
                                  class="mb-4"
                                >
                                  <p>
                                    Let’s come back to your galaxy spectrum. Notice your spectrum has some bright spikes or faint dips.
                                  </p>
                                  <p>
                                    The bright spikes are <strong>emission lines</strong>.
                                  </p>
                                  <p>
                                    The faint dips are <strong>absorption lines</strong>.
                                  </p>
                                  <p>
                                    One of the lines in your spectrum is labeled with an element symbol. Click the label to note the element line and its <strong>rest wavelength</strong> in your table.
                                  </p>
                                </div>

                                <div class="text-center my-8">
                                  <v-btn
                                    class="black--text"
                                    color="success"
                                    elevation="2"
                                    @click="
                                    "
                                  >
                                    click the label
                                  </v-btn>
                                </div>
                                <v-divider
                                  class="my-4"
                                >
                                </v-divider>

                                <v-row
                                  align="center"
                                  no-gutters
                                >
                                  <v-col>
                                    <v-btn
                                      class="black--text"
                                      color="accent"
                                      elevation="2"
                                      @click="
                                        state.marker = 'mee_spe1';
                                      "
                                    >
                                      back
                                    </v-btn>
                                  </v-col>
                                  <v-spacer></v-spacer>
                                  <v-col
                                    class="shrink"
                                  >
                                    <v-btn
                                      color="accent"
                                      class="black--text"
                                      elevation="2"
                                      @click="
                                        state.marker = 'obs_wav1';
                                      "
                                    >
                                      next
                                    </v-btn>
                                  </v-col>
                                </v-row>
                              </v-alert>

                              <!-- GUIDANCE ALERT - Observed Wavelength #1 -->
                              <v-alert
                                :class="state.marker == 'obs_wav1' ? 'd-block' : 'd-none'"
                                class="mb-4"
                                color="info"
                                elevation="6"
                              >
                                <h3
                                  class="mb-4"
                                >
                                  Observed Wavelength
                                </h3>
                                <div
                                  class="mb-4"
                                >
                                  <p>
                                    Your line’s rest wavelength has been recorded in the table.
                                  </p>
                                  <p>
                                    Now let’s measure the <strong>observed wavelength</strong> of the line.
                                  </p>
                                  <p>
                                    Slide the vertical measuring tool until it aligns with the line you identified, and click to record the line’s observed wavelength in the table.
                                  </p>
                                </div>

                                <div class="text-center my-8">
                                  <v-btn
                                    class="black--text"
                                    color="success"
                                    elevation="2"
                                    @click="
                                    "
                                  >
                                    align tool to line
                                  </v-btn>
                                </div>
                                <v-divider
                                  class="my-4"
                                >
                                </v-divider>

                                <v-row
                                  align="center"
                                  no-gutters
                                >
                                  <v-col>
                                    <v-btn
                                      class="black--text"
                                      color="accent"
                                      elevation="2"
                                      @click="
                                        state.marker = 'res_wav1';
                                      "
                                    >
                                      back
                                    </v-btn>
                                  </v-col>
                                  <v-spacer></v-spacer>
                                  <v-col
                                    class="shrink"
                                  >
                                    <v-btn
                                      color="accent"
                                      class="black--text"
                                      elevation="2"
                                      @click="
                                        state.marker = 'rep_rem1';
                                      "
                                    >
                                      next
                                    </v-btn>
                                  </v-col>
                                </v-row>
                              </v-alert>

                              <!-- GUIDANCE ALERT - Repeat for Remaining Galaxies #1 -->
                              <v-alert
                                :class="state.marker == 'rep_rem1' ? 'd-block' : 'd-none'"
                                class="mb-4"
                                color="info"
                                elevation="6"
                              >
                                <h3
                                  class="mb-4"
                                >
                                  Repeat for Remaining Galaxies
                                </h3>
                                <div
                                  class="mb-4"
                                >
                                  <p>
                                    Your measurement of the line’s observed wavelength is now recorded in the table.
                                  </p>
                                  <p>
                                    Repeat these measurements for your 4 remaining galaxies.
                                  </p>
                                </div>

                                <div class="text-center my-8">
                                  <v-btn
                                    class="black--text"
                                    color="success"
                                    elevation="2"
                                    @click="
                                      state.gal_snackbar = 0;
                                      state.dist_snackbar = 0;
                                      state.marker_snackbar = 0;
                                      state.vel_snackbar = 0;
                                      state.data_ready_snackbar = 0;
                                      state.marker_snackbar = 1;
                                      state.waveline_set = 1;
                                    "
                                  >
                                    repeat 4 times
                                  </v-btn>
                                </div>
                                <v-divider
                                  class="my-4"
                                >
                                </v-divider>

                                <v-row
                                  align="center"
                                  no-gutters
                                >
                                  <v-col>
                                    <v-btn
                                      class="black--text"
                                      color="accent"
                                      elevation="2"
                                      @click="
                                        state.marker = 'obs_wav1';
                                      "
                                    >
                                      back
                                    </v-btn>
                                  </v-col>
                                  <v-spacer></v-spacer>
                                  <v-col
                                    class="shrink"
                                  >
                                    <v-btn
                                      color="accent"
                                      class="black--text"
                                      elevation="2"
                                      @click="
                                        state.marker = 'nic_wor1';
                                      "
                                    >
                                      next
                                    </v-btn>
                                  </v-col>
                                </v-row>
                              </v-alert>

                              <!-- GUIDANCE ALERT - Nice Work #1 -->
                              <v-alert
                                :class="state.marker == 'nic_wor1' ? 'd-block' : 'd-none'"
                                class="mb-4"
                                color="info"
                                elevation="6"
                              >
                                <h3
                                  class="mb-4"
                                >
                                  Nice Work
                                </h3>
                                <div
                                  class="mb-4"
                                >
                                  <p>
                                    Now let’s examine what conclusions you might draw from your data.
                                  </p>
                                </div>
                                <v-divider
                                  class="my-4"
                                >
                                </v-divider>

                                <v-row
                                  align="center"
                                  no-gutters
                                >
                                  <v-col>
                                    <v-btn
                                      class="black--text"
                                      color="accent"
                                      elevation="2"
                                      @click="
                                        state.marker = 'rep_rem1';
                                      "
                                    >
                                      back
                                    </v-btn>
                                  </v-col>
                                  <v-spacer></v-spacer>
                                  <v-col
                                    class="shrink"
                                  >
                                    <v-btn
                                      disabled
                                      color="accent"
                                      class="black--text"
                                      elevation="2"
                                      @click="
                                        state.marker = 'nic_wor1';
                                      "
                                    >
                                      next
                                    </v-btn>
                                  </v-col>
                                </v-row>
                              </v-alert>

                              <v-row>
                                <v-col
                                  cols="6"
                                >
                                  <!-- FORM DIALOG as template for reflections/MC -->
                                  <guide-specvel-windows
                                    button-text="info"
                                    close-text="done"
                                    @close="
                                      console.log('Done button was clicked.');
                                      state.vel_win_unopened = 0;d
                                    "
                                  >
                                  </guide-specvel-windows>
                                </v-col>
                                <v-col
                                  cols="6"
                                >
                                  <span
                                    :class="state.waveline_set ? 'd-block' : 'd-none'"
                                  >
                                    <!-- FORM DIALOG as template for reflections/MC -->
                                    <reflect-velocity-windows
                                      button-text="do"
                                      close-text="submit"
                                      @submit="
                                        console.log('Submit button was clicked.');
                                      "
                                    >
                                    </reflect-velocity-windows>
                                  </span>
                                </v-col>
                              </v-row>
                            </v-col>
                          </v-row>
                        </v-container>


                        <!-- Sample DIALOGS/ALERTS for Learning Experience -->
                        <v-divider
                          class="my-4"
                        >
                        </v-divider>
                        <v-container>
                          <v-row>
                            <v-col
                              cols="12"
                            >
                              <template>
                                <v-row justify="center">
                                  <v-col cols="12">
                                    <v-expansion-panels
                                      accordion
                                      :class="state.darkmode ? 'theme--dark' : 'theme--light'"
                                    >
                                      <v-expansion-panel
                                        key="1"
                                      >
                                        <v-expansion-panel-header>Scaffolded Experience</v-expansion-panel-header>
                                        <v-expansion-panel-content>

                                          <!-- WIREFRAME of Dialogs/Alerts for Student Experience and Learning Objectives -->
                                          <infodialog-alert>
                                            $$ x = \frac{\input[my-id][my-class my-class-2]{} - 1}{\input[my-id-2][my-class]{}} $$
                                            This window provides a view of the "night sky". As you explore this view,
                                            you may see stars, nebulae, and galaxies.<br>
                                            <b>Pan:</b> click + drag (or use the W-A-S-D keys)<br>
                                            <b>Zoom:</b> scroll in and out (or use the I-O keys for finer zoom)<br>
                                            Once you feel comfortable navigating in the viewer, click "next"
                                          </infodialog-alert>
                                          <teamaside-alert>
                                            Load galaxy position markers.
                                          </teamaside-alert>
                                          <teamaside-alert>
                                            (Depending on sky density of final data set, we may need to think through the UX
                                            if students have trouble panning in the sky because they keep accidentally
                                            clicking on galaxies that get added to their table.) 
                                          </teamaside-alert>
                                          <infodialog-alert>
                                            Now let's take a look at your galaxy's spectrum. Recall that a spectrograph separates
                                            light from a source into its distinct colors. The spectrum graph shows how bright the
                                            light from the galaxy is at each color. Notice that the spectrum has one or more upward
                                            spiky lines that are very bright (emission lines) or downward dips that are faint
                                            (absorption lines). These lines are caused by specific atoms and molecules in the galaxy
                                            emitting or absorbing light at those particular colors. Look for one of the lines
                                            labeled as Hydrogen (H), Calcium (Ca), or Potassium (K).<br>

                                            Click on the element label to record its rest wavelength in your table.
                                          </infodialog-alert>
                                          <teamaside-alert>
                                            Element and rest wavelength appear in table.
                                          </teamaside-alert>
                                          <infodialog-alert>
                                            Click on the vertical measuring tool and drag it to line up with the labeled line.
                                            Click again to record the observed wavelength of that line.
                                          </infodialog-alert>
                                          <infodialog-alert>
                                            Notice your wavelength measurement is now recorded in the table.
                                          </infodialog-alert>
                                          <infodialog-alert>
                                            Repeat this process for four more galaxies (or however many your instructor would like
                                            you to collect data for).
                                          </infodialog-alert>
                                          <teamaside-alert>
                                            The reflection alerts below will need to be converted to components that have proper
                                            multiple choice functionality wired up.
                                          </teamaside-alert>
                                          <responsedialog-alert>
                                            How do the observed wavelengths of emission or absorption lines in your galaxies compare
                                            with the “rest” wavelength of those lines?
                                            <ul>
                                              <li>Lines in the galaxies have the same wavelength as the lines at rest
                                              <li>Some galaxies have lines with smaller wavelengths and some have lines with larger
                                                wavelengths than the lines at rest
                                              <li>Most or all of the galaxies have lines with smaller wavelengths than the lines at rest
                                              <li>Most or all of the galaxies have lines with larger wavelengths than the lines at rest.
                                            </ul>
                                          </responsedialog-alert>
                                          <responsedialog-alert>
                                            Reflect on what you can conclude from the data you just collected about how the galaxies are
                                            moving relative to our home galaxy, the Milky Way:
                                            <ul>
                                              <li>The galaxies are not moving.
                                              <li>Some galaxies are moving toward our galaxy and some galaxies are moving away from our galaxy.
                                              <li>Galaxies are mostly moving toward our galaxy.
                                              <li>Galaxies are mostly moving away from our galaxy.
                                            </ul>
                                          </responsedialog-alert>
                                          <responsedialog-alert>
                                            Now that we agree these galaxies are not static, let’s calculate how fast these galaxies are moving. 
                                          </responsedialog-alert>
                                          <teamaside-alert>
                                            Display interface that shows how to calculate velocity.
                                            Once they've been through it once correctly, display a button they can click to make the rest of the velocities appear.
                                          </teamaside-alert>
                                          <responsedialog-alert>
                                            These were the prevailing viewpoints in the 1920's:
                                            <ul>
                                              <li> "The universe is static and unchanging"
                                              <li> "Galaxies in the universe are moving randomly"
                                            </ul>

                                            Do you data support either of these conclusions? What would you tell a scientist from 1920
                                            regarding the prevailing wisdom about galaxies during this time?
                                          </responsedialog-alert>
                                          <responsedialog-alert>
                                            How confident do you feel about the information you gave to the 1920 scientist based on your\
                                            data? What would improve your confidence in your data and ideas?
                                          </responsedialog-alert>

                                        </v-expansion-panel-content>
                                      </v-expansion-panel>
                                    </v-expansion-panels>
                                  </v-col>
                                </v-row>
                              </template>
                            </v-col>
                          </v-row>
                        </v-container>

                      </v-stepper-content>


                      <!-- ---------------- --------------------------------- ---------------- -->
                      <!-- ---------------- SECOND PAGE: DISTANCE MEASUREMENT ---------------- -->
                      <!-- ---------------- --------------------------------- ---------------- -->
                      <v-stepper-content step="2">

                        <v-container>
                          <v-row
                            class="d-flex align-stretch"
                          >
                            <!-- This WWT viewer widget allows user to select a galaxy; galaxy positions plotted by RA/Dec.
                            It will zoom in to chosen galaxy & put controls/instructions on screen. -->
                            <!-- viewers.wwt_viewer doesn't need to be prepended with "state" because it comes from "Application" in app.py, not "ApplicationState"-->
                            <v-col cols="12" md="8"
                              class="wwt_column"
                            >
                              <!-- WWT WIDGET to frame galaxy for Distance Estimate -->
                              <v-card
                                class="align-self-stretch"
                              >
                                <v-app-bar
                                  color="secondary"
                                  dark
                                  dense
                                >
                                  <v-icon left>
                                    mdi-ruler
                                  </v-icon>

                                  <v-toolbar-title>Estimate Distance</v-toolbar-title>

                                  <v-spacer></v-spacer>

                                  <v-btn icon>
                                    <v-icon>mdi-information-outline</v-icon>
                                  </v-btn>
                                </v-app-bar>
                                <c-measuring-tool
                                  class="wwt_measuring_tool"
                                />
                              </v-card>
                            </v-col>

                            <!-- SIDEBAR COLUMN to hold galaxy details and Estimate Distance -->
                            <v-col cols="12" md="4">
                              <div
                                :class="state.gal_selected ? 'd-block' : 'd-none'"
                              >
                                <v-card
                                  color="warning"
                                  width="100%"
                                >
                                  <v-card-title>{{state.measuring_name || "Galaxy Name"}}</v-card-title>
                                  <v-card-text>
                                    <v-divider></v-divider>
                                    <v-list
                                      color="warning"
                                    >
                                      <v-list-item-content>
                                        <v-list-item-title>{{state.measuring_type || "Galaxy Type"}}</v-list-item-title>
                                        <v-list-item-subtitle>type</v-list-item-subtitle>
                                      </v-list-item-content>
                                      <v-list-item-content>
                                        <v-list-item-title>100,000 light years</v-list-item-title>
                                        <v-list-item-subtitle>assumed size</v-list-item-subtitle>
                                      </v-list-item-content>
                                      <v-list-item-content>
                                        <v-list-item-title>{{state.measuring_tool_height}}</v-list-item-title>
                                        <v-list-item-subtitle>field of view</v-list-item-subtitle>
                                      </v-list-item-content>
                                      <v-list-item-content>
                                        <v-list-item-title>{{state.measured_ang_size_str}}</v-list-item-title>
                                        <v-list-item-subtitle>measured angular size</v-list-item-subtitle>
                                      </v-list-item-content>
                                    </v-list>
                                    <v-divider></v-divider>
                                    <v-text-field
                                      :value="state.galaxy_dist"
                                      label="Estimated Distance"
                                      hint="click button below"
                                      persistent-hint
                                      class="mt-8 mb-4"
                                      suffix="Mpc"
                                      outlined
                                      readonly
                                      dense
                                    ></v-text-field>
                                    <v-btn
                                      block
                                      color="primary"
                                      dark
                                      class="px-auto"
                                      max-width="100%"
                                      :disabled="!state.measure_gal_selected || state.measured_ang_size === 0 || state.measuring_view_changing"
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
                            <p
                              v-if="state.warn_size"
                              style="color: red;"
                            >This angular size seems much larger than expected. Are you sure your measurements are lined up with a galaxy? Please try again.
                            </p>
                            <v-btn
                              class="white--text"
                              color="purple darken-2"
                              :disabled="!state.measure_gal_selected || state.measuring_view_changing"
                              @click="toggle_measuring()"
                            >{{ state.measuring_on ? "Stop Measuring" : "Start Measuring" }}
                            </v-btn>
                          </v-row>
                          <v-row>
                            <!-- SIDEBAR COLUMN for giving Instructions -->
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
                              <!-- TABLE for Galaxies and Velocity Measurements -->
                              <!-- Probably delete dist-table, but need to check what c-distance-table is first -->
                              <!-- <dist-table>
                              </dist-table> -->
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
                      </v-stepper-content>

                    <!-- This sets up the screen for the Analysis/data fitting step -->

                    <!-- Will need buttons/functionality for:
                        * drawing by eye/calculating/plotting best fit lines
                        * Choosing different data sets - student/class/all
                        * Plotting by galaxy type -->


                    <!-- ---------------- ------------------------- ---------------- -->
                    <!-- ---------------- THIRD PAGE: ALL THAT DATA ---------------- -->
                    <!-- ---------------- ------------------------- ---------------- -->

                    <!-- This sets up the screen for the Analysis/data fitting step -->
                      <v-stepper-content step="3">
                        <v-container>
                          <v-row>
                            <v-card
                                width="100%"
                                class="mx-2"
                            >
                              <!-- THE TAB TABS -->
                              <v-tabs
                                v-model="state.analysis_tabs"
                                grow
                                background-color="secondary"
                                dark
                              >
                                <v-tab
                                  key="my_data"
                                >
                                  my data
                                </v-tab>
                                <v-tab
                                  key="class_data"
                                >
                                  my class data
                                </v-tab>
                                <v-tab
                                  key="gal_data"
                                >
                                  galaxy type
                                </v-tab>
                                <v-tab
                                  key="prof_data"
                                >
                                  professional<br>science data
                                </v-tab>
                              </v-tabs>

                              <!-- THE TAB PANELS -->
                              <v-tabs-items
                                v-model="state.analysis_tabs"
                                class="no-transition"
                              >


                                <!-- ---------------- ------------------ ---------------- -->
                                <!-- ---------------- FIRST TAB: MY DATA ---------------- -->
                                <!-- ---------------- ------------------ ---------------- -->
                                <v-tab-item
                                  key="my_data"
                                  class="no-transition" 
                                >
                                  <v-container>
                                    <v-row>
                                      <!-- SIDEBAR COLUMN with buttons to Draw Fit and Calculate Best Fit -->
                                      <v-col
                                        cols="3"
                                        class="align-stretch"
                                      >
                                        <div
                                          class="d-flex mb-4"
                                        >


                                          <v-btn
                                            color="red"
                                            class="flex-grow-1 white--text"
                                            @click="
                                              state.points_plotted = true;
                                              show_fit_points();"
                                          >
                                            plot my points
                                            <v-spacer></v-spacer>
                                            <v-icon
                                              right
                                              dark
                                              class="px-4"
                                            >
                                              mdi-chart-scatter-plot
                                            </v-icon>
                                          </v-btn>
                                        </div>
                                        <div
                                          class="d-flex mb-4"
                                        >
                                          <v-btn
                                            :outlined="state.draw_on"
                                            :disabled="!state.points_plotted"
                                            color="orange"
                                            class="flex-grow-1 white--text"
                                            @click="handle_fitline_click()"
                                          >
                                            {{ state.bestfit_drawn ? 'erase fit line' : 'draw a fit line' }}
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
                                            :disabled="!state.points_plotted"
                                            color="teal lighten-1"
                                            class="flex-grow-1 white--text"
                                            @click="fit_lines({
                                              'viewer_id': 'hub_fit_viewer',
                                              'layers': [0]
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
                                        <!-- PLOTTING WIDGET to plot My Data -->
                                        <v-lazy>
                                          <jupyter-widget
                                            :widget="viewers.hub_fit_viewer"
                                          ></jupyter-widget>
                                        </v-lazy>
                                        <!-- TABLE to hold Galaxy, Velocity & Distance -->
                                        <c-fit-table />
                                      </v-col>
                                    </v-row>
                                    <v-row>
                                      <v-col>
                                        <!-- Card to hold an Informational VIDEO -->
                                        <v-card
                                          class="pa-8 mx-auto"
                                          elevation="3"
                                          outlined
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
                                      </v-col>
                                    </v-row>
                                  </v-container>
                                </v-tab-item>

                                <!-- ---------------- ------------------------------ ---------------- -->
                                <!-- ---------------- SECOND TAB: EXPLORE CLASS DATA ---------------- -->
                                <!-- ---------------- ------------------------------ ---------------- -->
                                <v-tab-item
                                  key="class_data"
                                  class="no-transition" 
                                >
                                  <v-container>
                                    <v-row>
                                      <!-- SIDEBAR COLUMN to Select Data and Fit Lines -->
                                      <v-col
                                        cols="3"
                                      >
                                        <v-list
                                          style="max-height: 300px"
                                          class="overflow-y-auto"
                                        >
                                          <v-list-item-group
                                            multiple
                                            v-model="state.hubble_comparison_selections"
                                          >
                                            <v-list-item
                                              v-for="(option, index) in ['My data', 'Class data', 'All Participant data']"
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
                                                    :color="['#0616f4', '#f0c470', 'red'][index]"
                                                  ></v-checkbox>
                                                </v-list-item-action>
                                              </template>
                                            </v-list-item>
                                          </v-list-item-group>
                                        </v-list>
                                        <v-btn
                                          block
                                          color="primary"
                                          @click="fit_lines({
                                            'viewer_id': 'hub_comparison_viewer'
                                          })"
                                        >
                                          Fit Lines
                                        </v-btn>
                                      </v-col>
                                      <v-col>
                                        <!-- PLOTTING WIDGET to plot Each Dataset -->
                                        <v-lazy>
                                          <jupyter-widget
                                            :widget="viewers.hub_comparison_viewer"
                                          ></jupyter-widget>
                                        </v-lazy>
                                      </v-col>
                                    </v-row>
                                    <v-row>
                                      <v-col>
                                        <!-- FORM DIALOG to learn steps to Estimate the Age of the Universe -->
                                        <v-card
                                          class="pa-8 mx-auto"
                                            elevation="3"
                                        >
                                          Complete these steps to discover how we can Estimate
                                          the age of universe by inverting our <em>H</em><sub>0</sub> value.
                                          <div class="text-center mt-4">
                                            <form-dialog
                                              button-text="estimate age of universe"
                                              title-text="How do we estimate age of the universe?"
                                              close-text="close"
                                              @close="console.log('Close button was clicked.')"
                                            >
                                              Scaffolded steps to calculate the age of the universe from the <em>H</em><sub>0</sub> value.
                                            </form-dialog>
                                          </div>
                                        </v-card>
                                      </v-col>
                                    </v-row>
                                    <v-lazy>
                                      <v-row>
                                        <v-col>
                                          <!-- TABS for Histograms -->
                                          <v-tabs>
                                            <v-tab key="hist_class">My class</v-tab>
                                            <v-tab key="hist_prob">All data</v-tab>
                                            <v-tab key="hist_sandbox">Sandbox</v-tab>
                                            <!-- My Class HISTOGRAM -->
                                            <v-tab-item key="hist_class">
                                              <v-container>
                                                <v-row>
                                                  <!-- SIDEBAR COLUMN for Data Selection -->
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
                                                                :color="['red', 'blue', 'green'][index]"
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
                                                    <!-- HISTOGRAM of My Class Data -->
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
                                            <!-- All Data HISTOGRAM -->
                                            <v-tab-item key="hist_prob">
                                              <v-container>
                                                <v-row>
                                                  <!-- SIDEBAR COLUMN for Data Selection -->
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
                                                          v-for="(option, index) in ['Student values','Class values']"
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
                                                                :color="['blue', 'orange'][index]"
                                                              ></v-checkbox>
                                                            </v-list-item-action>
                                                          </template>
                                                        </v-list-item>
                                                      </v-list-item-group>
                                                    </v-list>
                                                  </v-col>
                                                  <v-col>
                                                    <!-- HISTOGRAM of All Data -->
                                                    <v-lazy>
                                                      <jupyter-widget
                                                        style="height: 300px"
                                                        :widget="viewers.all_distr_viewer">
                                                      </jupyter-widget>
                                                    </v-lazy>
                                                  </v-col>
                                              </v-container>
                                            </v-tab-item>
                                            <!-- Sandbox HISTOGRAM -->
                                            <v-tab-item key="hist_sandbox">
                                              <v-container>
                                                <v-row>
                                                  <!-- SIDEBAR COLUMN for Data Selection -->
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
                                                                :color="['red', 'blue', '#f0c470', 'purple', 'green', 'black'][index]"
                                                              ></v-checkbox>
                                                            </v-list-item-action>
                                                          </template>
                                                        </v-list-item>
                                                      </v-list-item-group>
                                                    </v-list>
                                                  </v-col>
                                                  <v-col>
                                                    <!-- HISTOGRAM for Sandbox -->
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
                                  </v-container>
                                </v-tab-item>


                                <!-- ---------------- ---------------------------- ---------------- -->
                                <!-- ---------------- THIRD TAB: GALAXY MORPHOLOGY ---------------- -->
                                <!-- ---------------- ---------------------------- ---------------- -->
                                <v-tab-item
                                  key="gal_data"
                                  class="no-transition" 
                                >
                                  <v-container>
                                    <v-row>
                                      <!-- SIDEBAR COLUMN for data subset selection and Fit Lines -->
                                      <v-col
                                        cols="3"
                                      >
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
                                        <v-btn
                                          block
                                          color="primary"
                                          @click="fit_lines({
                                            'viewer_id': 'hub_morphology_viewer'
                                          })"
                                        >
                                          Fit Lines
                                        </v-btn>
                                      </v-col>
                                      <v-col>
                                        <!-- PLOTTING WIDGET for all galaxy types -->
                                        <v-lazy>
                                          <jupyter-widget
                                            :widget="viewers.hub_morphology_viewer"
                                          ></jupyter-widget>
                                        </v-lazy>
                                      </v-col>
                                    </v-row>
                                    <v-row>
                                      <v-col>
                                        <!-- PROCEDURAL DIALOG to learn steps to Estimate the Age of the Universe -->
                                        <v-card
                                          class="pa-8 mx-auto"
                                          elevation="3"
                                        >
                                          Buttons to calculate age of universe from <em>H</em><sub>0</sub> value.
                                          <div class="text-center mt-4">
                                            <form-dialog
                                              button-text="estimate age of universe"
                                              title-text="How do we estimate age of the universe?"
                                              close-text="close"
                                              @close="console.log('Close button was clicked.')"
                                            >
                                              Probably no dialog here. Just produce the age of the universe estimate from the <em>H</em><sub>0</sub> value.
                                            </form-dialog>
                                          </div>
                                        </v-card>
                                      </v-col>
                                    </v-row>
                                  </v-container>
                                </v-tab-item>
                                

                                <!-- ---------------- ----------------------------- ---------------- -->
                                <!-- ---------------- FOURTH TAB: PROFESSIONAL DATA ---------------- -->
                                <!-- ---------------- ----------------------------- ---------------- -->
                                <v-tab-item
                                  key="prof_data"
                                  class="no-transition" 
                                >
                                  <v-container>
                                    <v-row>
                                      <!-- SIDEBAR COLUMN to choose Subset data and Fit Lines -->
                                      <v-col
                                        cols="3"
                                      >
                                        <v-list
                                          style="max-height: 300px"
                                          class="overflow-y-auto"
                                        >
                                          <v-list-item-group
                                            multiple
                                            v-model="state.hubble_prodata_selections"
                                          >
                                          <!--
                                            <v-list-item
                                              v-for="(option, index) in ['My data', 'Class data', 'All data']"
                                              :key="index"
                                              :value="index"
                                            >
                                            -->
                                            <v-list-item
                                              v-for="(option, index) in ['My data', 'Hubble (1929)', 'HST Key Project (2001)', 'Supernova Ia (2004)']"
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
                                                    :color="['#0616f4', '#ee0df0', 'green', 'red'][index]"
                                                  ></v-checkbox>
                                                </v-list-item-action>
                                              </template>
                                            </v-list-item>
                                          </v-list-item-group>
                                        </v-list>
                                        <v-btn
                                          block
                                          color="primary"
                                          @click="fit_lines({
                                            'viewer_id': 'hub_prodata_viewer'
                                          })"
                                        >
                                          Fit Lines
                                        </v-btn>
                                      </v-col>
                                      <v-col>
                                        <!-- PLOTTING WIDGET for Professional Science Data -->
                                        <v-lazy>
                                          <jupyter-widget
                                            :widget="viewers.hub_prodata_viewer"
                                          ></jupyter-widget>
                                        </v-lazy>
                                      </v-col>
                                    </v-row>
                                    <v-row>
                                      <v-col>
                                        <!-- PROCEDURAL DIALOG to learn steps to Estimate the Age of the Universe -->
                                        <v-card
                                          class="pa-8 mx-auto"
                                          elevation="3"
                                        >
                                          Buttons to calculate age of universe from <em>H</em><sub>0</sub> value.
                                          <div class="text-center mt-4">
                                            <form-dialog
                                              button-text="estimate age of universe"
                                              title-text="How do we estimate age of the universe?"
                                              close-text="close"
                                              @close="console.log('Close button was clicked.')"
                                            >
                                              Probably no dialog here. Just produce the age of the universe estimate from the <em>H</em><sub>0</sub> value.
                                            </form-dialog>
                                          </div>
                                        </v-card>
                                      </v-col>
                                    </v-row>
                                  </v-container>
                                </v-tab-item>



                              </v-tabs-items>
                            </v-card>
                          </v-row>
                        </v-container>
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
                    <!-- for FINAL, use the following -- :disabled="state.over_model == 3 ? true : state.next1_disabled" -->
                    <v-btn
                      :disabled="false"
                      color="primary"
                      dark
                      @click="
                        state.over_model =
                          state.over_model < 3
                            ? state.over_model + 1
                            : state.over_model
                      "
                    >
                      {{ state.over_model == 3 ? 'Finish' : 'Next' }}
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
            <v-row
              class="mt-8"
            >
              <v-col cols="12">
                <!-- Sample DIALOGS/ALERTS for Learning Experience -->
                <v-divider
                  class="my-4"
                >
                </v-divider>
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
                  This is for student reflection pop-ups
                </responsedialog-alert>
                <todo-alert>
                  This is for tasks that still need to be completed
                </todo-alert>
                <teamaside-alert>
                  This is for notes to the team that won't be exposed to the user in finished DS
                </teamaside-alert>
              </v-col>
            </v-row>
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

<script>

export default {
  mounted() {
    window.MathJax = {
      tex: {packages: {'[+]': ['input']}},
      startup: {
        ready() {
          const Configuration = MathJax._.input.tex.Configuration.Configuration;
          const CommandMap = MathJax._.input.tex.SymbolMap.CommandMap;
          const TEXCLASS = MathJax._.core.MmlTree.MmlNode.TEXCLASS;
          
          new CommandMap('input', {input: 'Input'}, {
            Input(parser, name) {
              const xml = parser.create('node', 'XML');
              const id = parser.GetBrackets(name, '');
              const cls = parser.GetBrackets(name, '');
              const value = parser.GetArgument(name);
              xml.setXML(MathJax.startup.adaptor.node('input', {
                id: id, class: cls, value: value, xmlns: 'http://www.w3.org/1999/xhtml'
              }), MathJax.startup.adaptor);
              xml.getSerializedXML = function () {
                return this.adaptor.outerHTML(this.xml) + '</input>';
              }
              parser.Push(
                parser.create('node', 'TeXAtom', [
                  parser.create('node', 'semantics', [
                    parser.create('node', 'annotation-xml', [
                      xml
                    ], {encoding: 'application/xhtml+xml'})
                  ])
                ], {texClass: TEXCLASS.ORD})
              );
            }
          });
          Configuration.create('input', {handler: {macro: ['input']}});

          MathJax.startup.defaultReady();
        }
      }
    };

    // Grab MathJax itself
    const mathJaxScript = document.createElement('script');
    mathJaxScript.async = false;
    mathJaxScript.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js";
    document.head.appendChild(mathJaxScript);

    // Not all of our elements are initially in the DOM,
    // so we need to account for that in order to get MathJax
    // to render their formulae properly
    const mathJaxOpeningDelimiters = [ "$$", "\\(", "\\[" ];
    const containsMathJax = node => mathJaxOpeningDelimiters.some(delim => node.innerHTML.includes(delim));
    const elementToScan = node => node.nodeType === Node.ELEMENT_NODE;
    const mathJaxCallback = function(mutationList, _observer) {
      mutationList.forEach(mutation => {
        if (mutation.type === 'childList') {

          const needTypesetting = [];
          mutation.addedNodes.forEach(node => {
            if (elementToScan(node) && containsMathJax(node)) {
              needTypesetting.push(node);
            }
          });
          if (needTypesetting.length > 0) {
            MathJax.typesetPromise(needTypesetting);
          }

          const toClear = [];
          mutation.removedNodes.forEach(node => {
            if (elementToScan(node) && containsMathJax(node)) {
              toClear.push(node);
            }
          })
          if (toClear.length > 0) {
            MathJax.typesetClear(toClear);
          }
        }
      });
    }
    const observer = new MutationObserver(mathJaxCallback);
    const options = { childList: true, subtree: true };
    observer.observe(this.$el, options);
  }
}
</script>


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

.vuetify-styles .v-stepper__content {
  min-height: 500px;
  padding: 0px;
}

.v-tabs-items {
  min-height: 300px;
}

.no-transition .v-stepper__content {
  transition: none !important;
}

.no-transition {
  transition: none !important;
}

input {
  width: 1rem !important;
  border: 1px solid black !important;
  border-radius: 3px !important;
}

.MathJax, .MathJax_Display {
  width: fit-content;
  height: fit-content;
}

/* issues with empty headers pushing WWT widget south, anyone else having this problem? -HOH */
.wwt_column {
  overflow-y: hidden;
}

.wwt_widget .v-toolbar, .wwt_measuring_tool .v-toolbar {
  display: none;
}

.wwt_widget .v-card {
  overflow: hidden;
}


/* Styling for Galaxy table */
.galtable_column .v-card {
  min-height: 100%;
}

.galtable_column .v-data-table__wrapper {
  overflow-y: hidden;
}

.codeFont {
  font-family: 'Courier New';
}


</style>
