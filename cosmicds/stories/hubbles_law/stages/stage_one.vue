<template>
  <v-card class="mb-12">
    <v-container class="pt-0">
      <v-row>
        <v-col cols="6" class="wwt_column">
          <!-- WIDGET for WWT galaxy selection -->
          <div class="wwt_widget">
            <!-- WWT GALAXY PICKER as Jupyter Widget -- v-lazy loads when visible -->
            <v-lazy>
              <jupyter-widget :widget="viewers.wwt_viewer"></jupyter-widget>
            </v-lazy>
          </div>
        </v-col>
        <v-col cols="6" class="galtable_column">
          <!-- GUIDANCE ALERT - introduce students to WWT Viewer -->
          <v-alert
            :class="state.marker == 'exp_sky1' ? 'd-block' : 'd-none'"
            class="mb-4"
            color="info"
            elevation="6"
          >
            <h3 class="mb-4">Explore the Sky</h3>
            <div class="mb-4">
              This window provides a view of the night sky. As you explore this
              view, you may see stars, nebulae, and galaxies.
            </div>
            <div class="mb-2 mx-4">
              <v-row no-gutters class="mb-3">
                <v-col cols="3">
                  <strong>Pan</strong>
                </v-col>
                <v-col cols="9">
                  <strong>click + drag</strong><br />
                  (or use the <strong class="codeFont">I-J-K-L</strong> keys)
                </v-col>
              </v-row>
              <v-row no-gutters>
                <v-col cols="3">
                  <strong>Zoom</strong>
                </v-col>
                <v-col cols="9">
                  <strong>scroll in and out</strong><br />
                  (or use the <strong class="codeFont">Z-X</strong> keys for
                  finer zoom)
                </v-col>
              </v-row>
            </div>
            <v-divider class="my-4"> </v-divider>

            <v-row align="center" no-gutters>
              <v-col cols="8">
                Ready to proceed? Click <strong>NEXT</strong>.
              </v-col>
              <v-spacer></v-spacer>
              <v-col class="shrink">
                <v-btn
                  color="accent"
                  class="black--text"
                  elevation="2"
                  @click="state.marker = 'sel_gal1'"
                >
                  next
                </v-btn>
              </v-col>
            </v-row>
          </v-alert>

          <!-- GUIDANCE ALERT - introduce students to WWT Viewer -->
          <v-alert
            :class="state.marker == 'sel_gal1' ? 'd-block' : 'd-none'"
            class="mb-4"
            color="info"
            elevation="6"
          >
            <h3 class="mb-4">Select a Galaxy</h3>
            <div class="mb-4">
              The
              <strong
                :class="
                  state.darkmode
                    ? 'green--text text--lighten-2'
                    : 'green--text text--darken-1'
                "
                >green</strong
              >
              dots mark the locations of galaxies you can collect data for.
            </div>
            <div class="mb-4">
              Click on one of these dots to select that galaxy.
            </div>
            <v-divider class="my-4"> </v-divider>

            <v-row align="center" no-gutters>
              <v-spacer></v-spacer>
              <v-col class="shrink">
                <v-btn
                  color="accent"
                  class="black--text"
                  elevation="2"
                  @click="
                    state.marker = 'sel_gal2';
                    state.galaxy_table_visible = 1;
                    state.gal_snackbar = 0;
                    state.dist_snackbar = 0;
                    state.marker_snackbar = 0;
                    state.vel_snackbar = 0;
                    state.data_ready_snackbar = 0;
                    state.gal_snackbar = 1;
                    state.gals_total += 1;
                    add_galaxy_data_point();
                  "
                >
                  next
                </v-btn>
              </v-col>
            </v-row>
          </v-alert>
          <!-- TABLE to hold Selected Galaxies -->
          <c-galaxy-table
            :class="state.galaxy_table_visible ? 'd-block' : 'd-none'"
          />
        </v-col>
      </v-row>
      <v-row
        :class="
          (state.marker == 'sel_gal2') | 'cho_row1' ? 'd-block' : 'd-none'
        "
      >
        <v-col>
          <!-- GUIDANCE ALERT - Show students how to select galaxies -->
          <v-alert
            :class="state.marker == 'sel_gal2' ? 'd-block' : 'd-none'"
            color="info"
            class="mb-4"
            elevation="6"
          >
            <h3 class="mb-4">Select Five Galaxies</h3>
            <div class="mb-4">
              Notice that the table now has a row for your selected galaxy.
            </div>
            <div>
              Now pan around the sky and choose 4 more galaxies to enter into
              your table.
            </div>
            <v-divider class="my-4"> </v-divider>

            <v-row align="center" no-gutters>
              <v-col>
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
                    state.gal_snackbar = 1;
                    state.gal_selected = 1;
                    state.haro_on = 'd-block';
                    state.gals_total += 1;
                    add_galaxy_data_point();
                  "
                >
                  select galaxy ({{ state.gals_total }})
                </v-btn>
              </v-col>
              <v-spacer></v-spacer>

              <v-col
                cols="2"
                class="shrink"
                :class="state.gals_total < 5 ? 'd-block' : 'd-none'"
              >
                <div>Select 5 galaxies before moving on.</div>
              </v-col>
              <v-col
                class="shrink"
                :class="state.gals_total >= 5 ? 'd-block' : 'd-none'"
              >
                <v-btn
                  class="black--text"
                  color="accent"
                  elevation="2"
                  @click="state.marker = 'cho_row1'"
                >
                  move on to measuring
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
            <h3 class="mb-4">Choose a Row</h3>
            <div class="mb-4">
              Now let's take a look at the light spectrum for one of your
              galaxies.
            </div>
            <div>Click on a row in your table to choose that galaxy.</div>
            <v-divider class="my-4"> </v-divider>

            <v-row align="center" no-gutters>
              <v-spacer></v-spacer>
              <v-col class="shrink">
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
        <v-col cols="12" md="8" class="align-stretch">
          <!-- The CARD to hold the SPECTRUM TOOL and where students Measure Velocity -->
          <v-card
            :class="state.spectrum_tool_visible ? 'd-block' : 'd-none'"
            min-height="300px"
            outlined
            color="info"
            class="pa-1"
          >
            <v-toolbar color="secondary" dense dark>
              <v-toolbar-title>Spectrum Tool</v-toolbar-title>

              <v-spacer></v-spacer>

              <v-btn icon>
                <v-icon>mdi-information-outline</v-icon>
              </v-btn>
            </v-toolbar>
            <jupyter-widget :widget="viewers.spectrum_viewer"> </jupyter-widget>
          </v-card>
        </v-col>
        <!-- SIDEBAR COLUMN for processing velocity data -->
        <v-col cols="12" md="4">
          <!-- GUIDANCE ALERT - Introduce Spectrum Tool -->
          <v-alert
            :class="state.marker == 'mee_spe1' ? 'd-block' : 'd-none'"
            class="mb-4"
            color="info"
            elevation="6"
          >
            <h3 class="mb-4">Meet the Spectrum Tool</h3>
            <div class="mb-4">
              To the left is a spectrum of light from your chosen galaxy.
            </div>
            <div>
              Let’s learn how a spectrum can tell us if an object is moving
              toward or away from us.
            </div>
            <v-divider class="my-4"> </v-divider>

            <v-row align="center" no-gutters>
              <v-spacer></v-spacer>
              <v-col class="shrink">
                <!-- FORM DIALOG as template for reflections/MC -->
                <guide-specvel-windows
                  button-text="start"
                  close-text="submit"
                  @close="
                    console.log('Submit button was clicked.');
                    state.marker = 'mee_spe2';
                  "
                >
                </guide-specvel-windows>
              </v-col>
            </v-row>
          </v-alert>

          <!-- GUIDANCE ALERT - Spectrum Tool #2 -->
          <v-alert
            :class="state.marker == 'mee_spe2' ? 'd-block' : 'd-none'"
            class="mb-4"
            color="info"
            elevation="6"
          >
            <h3 class="mb-4">Meet the Spectrum Tool</h3>
            <div class="mb-4">
              Let’s come back to your galaxy spectrum. Notice your spectrum has
              some bright spikes or faint dips.
            </div>
            <div>The bright spikes are <strong>emission lines</strong>.</div>
            <div>The faint dips are <strong>absorption lines</strong>.</div>
            <div>
              Let’s learn how a spectrum can tell us if an object is moving
              toward or away from us.
            </div>
            <v-divider class="my-4"> </v-divider>

            <v-row align="center" no-gutters>
              <v-spacer></v-spacer>
              <v-col class="shrink">
                <v-btn
                  color="accent"
                  class="black--text"
                  elevation="2"
                  @click="state.marker = ''"
                >
                  next
                </v-btn>
              </v-col>
            </v-row>
          </v-alert>

          <!-- GUIDANCE DIALOG - Explore Spectra & Velocities - might be able to delete this if the button works in the alert   -->
          <v-container class="d-none">
            <v-row class="text-center">
              <v-col>
                <!-- FORM DIALOG as template for reflections/MC -->
                <reflect-velocity-windows
                  button-text="reflect"
                  close-text="submit"
                  @close="
                    console.log('Submit button was clicked.');
                    state.rv1_visible = 0;
                    state.calc_visible = 'd-block';
                  "
                >
                </reflect-velocity-windows>
              </v-col>
            </v-row>
          </v-container>

          <v-alert
            border="left"
            color="indigo"
            dark
            elevation="2"
            class="mb-12"
          >
            <!-- Our SME told me that E galaxies aren't likely to have H-alpha lines, so we will need to give
                              options for measuring other types of lines too, like Ca or K lines. We can figure this out once
                              we have the data set to look at.-->
            Use the mouse to drag the vertical wavelength marker until it lines
            up with the labeled absorption or emission line. Left-click to
            record the element and wavelength of the line.

            <!-- The click action will be on the spectrum itself, so we can remove this when it is active -->
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
                  state.rv1_visible = 1;
                "
              >
                set marker
              </v-btn>
            </div>
          </v-alert>
          <v-container :class="state.rv1_visible ? 'd-block' : 'd-none'">
            <v-row class="text-center">
              <v-col>
                <!-- FORM DIALOG as template for reflections/MC -->
                <reflect-velocity-windows
                  button-text="reflect"
                  close-text="submit"
                  @close="
                    console.log('Submit button was clicked.');
                    state.rv1_visible = 0;
                    state.calc_visible = 'd-block';
                  "
                >
                </reflect-velocity-windows>
              </v-col>
            </v-row>
          </v-container>

          <div :class="state.calc_visible">
            <!-- CARD to CALCULATE the velocity from the wavelength -->
            <v-card
              color="indigo lighten-5"
              class="mb-4"
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
                      ? (state.data_ready_snackbar = 1)
                      : (state.vel_snackbar = 1);
                    state.adddata_disabled =
                      state.dist_measured == 1 ? false : true;
                    state.galaxy_vel = Math.floor(Math.random() * 60000) + 5000;
                    state.vels_total += 1;
                  "
                >
                  calculate ({{ state.vels_total }})
                </v-btn>
              </v-card-text>
            </v-card>
          </div>

          <v-container :class="state.vels_total < 5 ? 'd-none' : 'd-block'">
            <v-row>
              <v-col cols="12">
                <!-- FORM DIALOG as template for reflections/MC -->
                <form-dialog
                  button-text="reflect"
                  title-text="Reflection Questions"
                  close-text="submit"
                  @close="console.log('Submit button was clicked.')"
                >
                  These were the prevailing viewpoints in the 1920's:
                  <ul class="mb-4">
                    <li><em>The universe is static and unchanging</em></li>
                    <li>
                      <em>Galaxies in the universe are moving randomly</em>
                    </li>
                  </ul>
                  <h3>Question 1</h3>
                  Do your data support either of these conclusions?
                  <form-textarea question-label="Question 1"> </form-textarea>
                  <h3>Question 2</h3>
                  What would you tell a scientist from 1920 regarding the
                  prevailing wisdom about galaxies during this time?
                  <form-textarea question-label="Question 2"> </form-textarea>
                  <h3>Question 3</h3>
                  Based on your data, how confident are you about what you told
                  the 1920's scientist? What would improve your confidence in
                  your data and conclusions?
                  <form-textarea question-label="Question 3"> </form-textarea>
                </form-dialog>
              </v-col>
            </v-row>
          </v-container>

          <!-- Card to hold an Informational VIDEO -->
          <v-card
            outlined
            class="pa-5 mt-8"
            color="orange lighten-5"
            elevation="0"
          >
            Watch this video for instructions on measuring wavelengths and
            velocities based on emission and absorption lines.

            <div class="text-center mt-4">
              <video-dialog
                button-text="learn more"
                title-text="How do we measure galaxy velocity?"
                close-text="close"
                @close="console.log('Close button was clicked.')"
              >
                Verbiage about comparing observed and rest wavelengths of
                absorption/emission lines
              </video-dialog>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Sample DIALOGS/ALERTS for Learning Experience -->
    <v-divider class="my-4"> </v-divider>
    <v-container>
      <v-row>
        <v-col cols="12">
          <template>
            <v-row justify="center">
              <v-col cols="12">
                <v-expansion-panels
                  accordion
                  :class="state.darkmode ? 'theme--dark' : 'theme--light'"
                >
                  <v-expansion-panel key="1">
                    <v-expansion-panel-header
                      >Scaffolded Experience</v-expansion-panel-header
                    >
                    <v-expansion-panel-content>
                      <!-- WIREFRAME of Dialogs/Alerts for Student Experience and Learning Objectives -->
                      <infodialog-alert>
                        $$ x = \frac{\input[my-id][my-class my-class-2]{} -
                        1}{\input[my-id-2][my-class]{}} $$ This window provides
                        a view of the "night sky". As you explore this view, you
                        may see stars, nebulae, and galaxies.<br />
                        <b>Pan:</b> click + drag (or use the W-A-S-D keys)<br />
                        <b>Zoom:</b> scroll in and out (or use the I-O keys for
                        finer zoom)<br />
                        Once you feel comfortable navigating in the viewer,
                        click "next"
                      </infodialog-alert>
                      <teamaside-alert>
                        Load galaxy position markers.
                      </teamaside-alert>
                      <infodialog-alert>
                        The (colored) dots mark the locations of galaxies you
                        can collect data for. Click on one of these dots to
                        select that galaxy.
                      </infodialog-alert>
                      <teamaside-alert>
                        (Depending on sky density of final data set, we may need
                        to think through the UX if students have trouble panning
                        in the sky because they keep accidentally clicking on
                        galaxies that get added to their table.)
                      </teamaside-alert>
                      <infodialog-alert>
                        Notice that the table now has a row for your selected
                        galaxy. "next"
                      </infodialog-alert>
                      <infodialog-alert>
                        Now let's take a look at your galaxy's spectrum. Recall
                        that a spectrograph separates light from a source into
                        its distinct colors. The spectrum graph shows how bright
                        the light from the galaxy is at each color. Notice that
                        the spectrum has one or more upward spiky lines that are
                        very bright (emission lines) or downward dips that are
                        faint (absorption lines). These lines are caused by
                        specific atoms and molecules in the galaxy emitting or
                        absorbing light at those particular colors. Look for one
                        of the lines labeled as Hydrogen (H), Calcium (Ca), or
                        Potassium (K).<br />

                        Click on the element label to record its rest wavelength
                        in your table.
                      </infodialog-alert>
                      <teamaside-alert>
                        Element and rest wavelength appear in table.
                      </teamaside-alert>
                      <infodialog-alert>
                        Click on the vertical measuring tool and drag it to line
                        up with the labeled line. Click again to record the
                        observed wavelength of that line.
                      </infodialog-alert>
                      <infodialog-alert>
                        Notice your wavelength measurement is now recorded in
                        the table.
                      </infodialog-alert>
                      <infodialog-alert>
                        Repeat this process for four more galaxies (or however
                        many your instructor would like you to collect data
                        for).
                      </infodialog-alert>
                      <teamaside-alert>
                        The reflection alerts below will need to be converted to
                        components that have proper multiple choice
                        functionality wired up.
                      </teamaside-alert>
                      <responsedialog-alert>
                        How do the observed wavelengths of emission or
                        absorption lines in your galaxies compare with the
                        “rest” wavelength of those lines?
                        <ul>
                          <li>
                            Lines in the galaxies have the same wavelength as
                            the lines at rest
                          </li>
                          <li>
                            Some galaxies have lines with smaller wavelengths
                            and some have lines with larger wavelengths than the
                            lines at rest
                          </li>

                          <li>
                            Most or all of the galaxies have lines with smaller
                            wavelengths than the lines at rest
                          </li>
                          <li>
                            Most or all of the galaxies have lines with larger
                            wavelengths than the lines at rest.
                          </li>
                        </ul>
                      </responsedialog-alert>
                      <responsedialog-alert>
                        Reflect on what you can conclude from the data you just
                        collected about how the galaxies are moving relative to
                        our home galaxy, the Milky Way:
                        <ul>
                          <li>The galaxies are not moving.</li>
                          <li>
                            Some galaxies are moving toward our galaxy and some
                            galaxies are moving away from our galaxy.
                          </li>
                          <li>Galaxies are mostly moving toward our galaxy.</li>
                          <li>
                            Galaxies are mostly moving away from our galaxy.
                          </li>
                        </ul>
                      </responsedialog-alert>
                      <responsedialog-alert>
                        Now that we agree these galaxies are not static, let’s
                        calculate how fast these galaxies are moving.
                      </responsedialog-alert>
                      <teamaside-alert>
                        Display interface that shows how to calculate velocity.
                        Once they've been through it once correctly, display a
                        button they can click to make the rest of the velocities
                        appear.
                      </teamaside-alert>
                      <responsedialog-alert>
                        These were the prevailing viewpoints in the 1920's:
                        <ul>
                          <li>"The universe is static and unchanging"</li>
                          <li>
                            "Galaxies in the universe are moving randomly"
                          </li>
                        </ul>

                        Do you data support either of these conclusions? What
                        would you tell a scientist from 1920 regarding the
                        prevailing wisdom about galaxies during this time?
                      </responsedialog-alert>
                      <responsedialog-alert>
                        How confident do you feel about the information you gave
                        to the 1920 scientist based on your\ data? What would
                        improve your confidence in your data and ideas?
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
  </v-card>
</template>