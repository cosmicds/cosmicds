<template>
  <div
    id="selection-root"
  >
    <v-toolbar
      color="secondary"
      dense
      dark
    >
      <v-toolbar-title>Night Sky Viewer</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-tooltip top>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon
            v-bind="attrs"
            v-on="on"
            @click="reset()">
            <v-icon>mdi-home</v-icon>
          </v-btn>
        </template>
        Reset view
      </v-tooltip>

      <v-btn icon>
        <v-icon>mdi-information-outline</v-icon>
      </v-btn>

    </v-toolbar>
    <jupyter-widget
      :widget="widget"
      class="wwt-widget"
    />
    <v-tooltip top>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          fab
          dark
          bottom
          right
          absolute
          color="secondary"
          class="selection-fab"
          v-bind="attrs"
          v-on="on"
          v-show="Object.keys(current_galaxy).length !== 0"
          @click="select_current_galaxy()">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </template>
      Add to my dataset
    </v-tooltip>
  </div>
</template>

<style scoped>
#selection-root {
  --toolbar-height: 48px;
  --widget-height: 400px;
  height: calc(var(--toolbar-height) + var(--widget-height));
  width: 100%;
}

.wwt-widget {
  height: 400px;
}

.selection-fab {
  --margin: 15px;
  --card-padding: 16px;
  bottom: 0px !important;
  margin-bottom: var(--margin);
  margin-right: calc(var(--margin) - var(--card-padding));
}

.wwt-widget .p-Widget, .wwt-widget iframe {
  height: 400px !important;
  width: 100% !important;
}
</style>
