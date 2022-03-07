<template>
  <v-card
    id="selection-root"
    color="info"
    class="pa-1"
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

    <v-tooltip top>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon
          v-bind="attrs"
          v-on="on"
          :disabled="Object.keys(current_galaxy).length === 0"
          @click="select_current_galaxy()">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </template>
      Add to my dataset
    </v-tooltip>

    <v-btn icon>
      <v-icon>mdi-information-outline</v-icon>
    </v-btn>
  </v-toolbar>
    <jupyter-widget
      :widget="widget"
      id="widget"
    />
  </v-card>
</template>
