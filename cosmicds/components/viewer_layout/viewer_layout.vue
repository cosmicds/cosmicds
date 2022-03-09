<template>
  <v-card flat>
    <v-toolbar
      dense
      dark
      color="secondary"
      v-if="show_toolbar">
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <jupyter-widget :widget="controls.toolbar_selection_tools"></jupyter-widget>
      </v-toolbar-items>
    </v-toolbar>
    <jupyter-widget :style="css_style" :widget="figure"></jupyter-widget>
  </v-card>
</template>
