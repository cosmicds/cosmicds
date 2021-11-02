<template>
  <v-app id="inspire">
    <v-app-bar
      app
      color="primary"
      dark
      src="https://cdn.eso.org/images/screen/eso1738b.jpg"
      clipped-right
      flat
      height="72"
    >
      <template v-slot:img="{ props }">
        <v-img
          v-bind="props"
          gradient="to top right, rgba(100,115,201,.7), rgba(25,32,72,.7)"
        ></v-img>
      </template>

      <v-app-bar-nav-icon @click="state.drawer = !state.drawer"></v-app-bar-nav-icon>

      <v-toolbar-title class="mr-5">
        <h2>Hubble's Law</h2>
      </v-toolbar-title>

      <v-toolbar-title> Cosmic Data Stories </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-responsive max-width="156">
        <v-text-field
          dense
          flat
          hide-details
          rounded
          solo-inverted
        ></v-text-field>
      </v-responsive>
    </v-app-bar>

    <v-navigation-drawer v-model="state.drawer" app width="300">
      <v-sheet color="grey lighten-5" height="72" width="100%">
        <v-list class="ma-0 pa-0">
          <v-list-item>
            <v-list-item-action>
              <v-avatar color="indigo">
                <v-icon dark> mdi-account-circle </v-icon>
              </v-avatar>
            </v-list-item-action>

            <v-list-item-content>
              <v-list-item-title>Nicholas Earl</v-list-item-title>
              <v-list-item-subtitle
                >nearl@gluesolutions.io</v-list-item-subtitle
              >
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-sheet>

      <v-stepper v-model="state.step" vertical flat class="elevation-0">
        <v-stepper-step :complete="state.step > 0" step="0">
          Collect Galaxy Data
          <small>Summarize if needed</small>
        </v-stepper-step>

        <v-stepper-content step="0">
          <v-skeleton-loader
            class="mb-6"
            boilerplate
            type="article"
          ></v-skeleton-loader>
          <v-btn color="primary" @click="state.step = 1"> Continue </v-btn>
          <v-btn text> Cancel </v-btn>
        </v-stepper-content>

        <v-stepper-step :complete="state.step > 1" step="1">
          Estimate Age of Universe
        </v-stepper-step>

        <v-stepper-content step="1">
          <v-skeleton-loader
            class="mb-6"
            boilerplate
            type="article"
          ></v-skeleton-loader>
          <v-btn color="primary" @click="state.step = 0"> Continue </v-btn>
          <v-btn text> Cancel </v-btn>
        </v-stepper-content>

        <!-- <v-stepper-step :complete="state.step > 3" step="3">
          Select an ad format and name ad unit
        </v-stepper-step>

        <v-stepper-content step="3">
          <v-skeleton-loader
            class="mb-6"
            boilerplate
            type="article"
          ></v-skeleton-loader>
          <v-btn color="primary" @click="state.step = 4"> Continue </v-btn>
          <v-btn text> Cancel </v-btn>
        </v-stepper-content>

        <v-stepper-step step="4"> View setup instructions </v-stepper-step>
        <v-stepper-content step="4">
          <v-skeleton-loader
            class="mb-6"
            boilerplate
            type="article"
          ></v-skeleton-loader>
          <v-btn color="primary" @click="state.step = 1"> Continue </v-btn>
          <v-btn text> Cancel </v-btn>
        </v-stepper-content> -->
      </v-stepper>
    </v-navigation-drawer>

    <v-navigation-drawer app clipped right>
      <v-list>
        <v-list-item v-for="n in 5" :key="n" link>
          <v-list-item-content>
            <v-list-item-title>Item {{ n }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-content>
        <v-container fluid>
          <v-tabs-items v-model="state.step">
            <v-tab-item v-for="stage in stages" :key="stage">
              <jupyter-widget :widget=stage />
            </v-tab-item>
          </v-tabs-items>
        </v-container>
      </v-content>
    </v-main>

    <v-footer app color="primary lighten-2" padless inset>
      <v-row justify="center" no-gutters>
        <v-col class="primary lighten-2 py-2 text-center white--text" cols="12">
          {{ new Date().getFullYear() }} — <strong>CosmicDS</strong>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script>
export default {};
</script>
