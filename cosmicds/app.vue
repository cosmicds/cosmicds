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

      <v-toolbar-title>Hubble Data Story</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main id="scrolling-techniques-4" class="overflow-y-auto fill-height">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" xl="8">
            <v-card class="d-flex flex-column">
              <v-stepper v-model="state.over_model" class="elevation-0">
                <v-stepper-header>
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
                    Analysis Tools
                  </v-stepper-step>

                  <v-divider></v-divider>

                  <v-stepper-step
                    :complete="state.over_model > 3"
                    step="3"
                    editable
                    >View Results</v-stepper-step
                  >
                </v-stepper-header>

                <v-stepper-items class="">
                  <v-stepper-content step="1">
                    <jupyter-widget
                      style="height: 300px"
                      :widget="viewers.hub_const_viewer"
                    ></jupyter-widget>

                    <v-card color="blue lighten-5" class="" flat>
                      <v-tabs
                        v-model="state.col_tab_model"
                        grow
                        background-color="blue lighten-4"
                      >
                        <v-tab key="gal-dist"> Estimate Galaxy Distance </v-tab>
                        <v-tab key="gal-vel"> Measure Galaxy Velocity </v-tab>
                      </v-tabs>

                      <v-tabs-items
                        v-model="state.col_tab_model"
                        style="background-color: transparent"
                        class="px-3"
                      >
                        <v-tab-item key="gal-dist">
                          <v-window v-model="state.est_model">
                            <v-window-item key="gal-select">
                              <v-row>
                                <v-col cols="12" md="4">
                                  <v-alert
                                    border="top"
                                    colored-border
                                    type="info"
                                    elevation="2"
                                  >
                                    Pan the sky and select one of the galaxies
                                    to measure.
                                  </v-alert>
                                </v-col>
                                <v-col cols="12" md="8">
                                  <jupyter-widget
                                    style="height: 300px"
                                    :widget="viewers.gal_viewer"
                                  ></jupyter-widget
                                ></v-col>
                              </v-row>
                            </v-window-item>
                            <v-window-item key="gal-size">
                              <v-row>
                                <v-col cols="12" md="4">
                                  <v-card class="fill-height">
                                    <v-card-title>Select Galaxy</v-card-title>
                                    <v-card-text>
                                      Type: Assumed size: Height of display:
                                    </v-card-text>
                                  </v-card>
                                </v-col>
                                <v-col cols="12" md="8">
                                  <jupyter-widget
                                    style="min-height: 300px"
                                    :widget="viewers.wwt_viewer"
                                  ></jupyter-widget
                                ></v-col>
                              </v-row>
                            </v-window-item>
                          </v-window>
                          <v-card-actions class="justify-space-between">
                            <v-btn
                              text
                              @click="
                                state.est_model =
                                  state.est_model - 1 < 0
                                    ? 0
                                    : state.est_model - 1
                              "
                            >
                              <v-icon>mdi-chevron-left</v-icon>
                            </v-btn>
                            <v-item-group
                              v-model="state.est_model"
                              class="text-center"
                              mandatory
                            >
                              <v-item
                                v-for="n in 2"
                                :key="`btn-${n}`"
                                v-slot="{ active, toggle }"
                              >
                                <v-btn
                                  :input-value="active"
                                  icon
                                  @click="toggle"
                                >
                                  <v-icon>mdi-record</v-icon>
                                </v-btn>
                              </v-item>
                            </v-item-group>
                            <v-btn
                              text
                              @click="
                                state.est_model =
                                  state.est_model + 1 > 1
                                    ? 1
                                    : state.est_model + 1
                              "
                            >
                              <v-icon>mdi-chevron-right</v-icon>
                            </v-btn>
                          </v-card-actions>
                        </v-tab-item>

                        <v-tab-item key="gal-vel"> </v-tab-item>
                      </v-tabs-items>
                    </v-card>
                  </v-stepper-content>

                  <v-stepper-content step="2">
                    <v-card
                      class="fill-height mb-12"
                      color="grey lighten-1 elevation-0"
                    ></v-card>

                    <v-btn color="primary" @click="state.over_model = 3">
                      Continue
                    </v-btn>

                    <v-btn text> Cancel </v-btn>
                  </v-stepper-content>

                  <v-stepper-content step="3">
                    <v-card
                      class="fill-height mb-12"
                      color="grey lighten-1 elevation-0"
                    ></v-card>

                    <v-btn color="primary" @click="state.over_model = 1">
                      Continue
                    </v-btn>

                    <v-btn text> Cancel </v-btn>
                  </v-stepper-content>
                </v-stepper-items>
              </v-stepper>
              <v-spacer></v-spacer>
              <v-divider></v-divider>
              <v-card-actions>
                <v-btn
                  color="primary"
                  @click="add_data_to_viewers(['hub_const_viewer', 'wwt_viewer'])"
                >
                  (Test) Add Data
                </v-btn>
                <v-btn
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

                <v-btn
                  color="primary"
                  @click="
                    state.over_model =
                      state.over_model < 3
                        ? state.over_model + 1
                        : state.over_model
                  "
                >
                  Next
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
        <c-footer />
      </v-container>
    </v-main>
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
</style>
