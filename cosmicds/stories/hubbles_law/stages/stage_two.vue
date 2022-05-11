<template>
  <v-container>
    <v-row>
      <v-col cols="1">
        <v-btn
          @click="story_state.stage_index = 1"
        >back</v-btn>
        <v-btn
          @click="story_state.start_over()"
        >start over</v-btn>
      </v-col>
    </v-row>
    <v-row class="d-flex align-stretch">
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
