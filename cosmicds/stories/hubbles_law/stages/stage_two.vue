<template>
  <v-container>
    <v-row class="d-flex align-stretch">
      <v-col cols="6">
        <v-card class="align-self-stretch">
          <c-distance-tool />
        </v-card>
      </v-col>
      <v-col cols="3">
        <c-distance-sidebar />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <jupyter-widget :widget="widgets.distance_table" />
      </v-col>
      <v-col cols="3">
        <c-angsize-slideshow />
      </v-col>
    </v-row>
  </v-container>
</template>
