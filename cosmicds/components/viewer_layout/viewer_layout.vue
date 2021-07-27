<template>
  <v-card flat>
    <v-toolbar flat short>
      <v-toolbar-items>
        <jupyter-widget :widget="controls.toolbar_selection_tools"></jupyter-widget>
      </v-toolbar-items>
    </v-toolbar>
    <jupyter-widget :style="css_style" :widget="figure"></jupyter-widget>
  </v-card>
</template>