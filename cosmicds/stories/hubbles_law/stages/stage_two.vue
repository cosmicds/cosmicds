<template>
  <v-container>
    <v-row class="d-flex align-stretch">
      <v-btn
        @click="story_state.stage_index = 1"
      >back</v-btn>
      <v-col cols="6">
        <v-card class="align-self-stretch">
          <c-distance-tool/>
        </v-card>
      </v-col>
      <v-col cols="3">
        <c-distance-sidebar/>
      </v-col>
    </v-row>
    <v-row>
      <jupyter-widget :widget="widgets.distance_table"/>
    </v-row>
  </v-container>
</template>
