<template>
  <v-container>
    <v-row>
      <v-col cols="6">
        <jupyter-widget :widget="widgets.fit_table"/>
      </v-col>
      <v-col cols="6">
        <jupyter-widget :widget="viewers.morphology_viewer"/>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <jupyter-widget :widget="viewers.fit_viewer"/>
      </v-col>
      <v-col cols="6">
        <jupyter-widget :widget="viewers.comparison_viewer"/>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <jupyter-widget :widget="viewers.class_distr_viewer"/>
      </v-col>
      <v-col cols="6">
        <jupyter-widget :widget="viewers.all_distr_viewer"/>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <jupyter-widget :widget="viewers.sandbox_distr_viewer"/>
      </v-col>
    </v-row>
  </v-container>
</template>
