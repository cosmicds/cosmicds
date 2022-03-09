<template>
  <v-container>
    <v-row>
      <v-btn
        color="green"
        @click="select_galaxies()"
      >select 5 galaxies</v-btn>
    </v-row>
    <v-row>
      <v-col
        cols="6">
        <v-card
          color="info"
          class="pa-1">
          <c-selection-tool/>
          <!-- <v-card-actions>
            <v-btn @click="story_state.step_index += 1; story_state.step_complete = true">Next Step</v-btn>
          </v-card-actions> -->
        </v-card>
      </v-col>
      <v-col
        cols="6">
          <jupyter-widget :widget="widgets.galaxy_table"/>
      </v-col>
    </v-row>
    <v-row>
      <c-select-guidance />
    </v-row>
    <v-row>
      <v-col
        cols="6">
        <v-card
          color="info"
          class="pa-1">
          <jupyter-widget :widget="viewers.spectrum_viewer"/>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
