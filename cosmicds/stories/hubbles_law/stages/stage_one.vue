<template>
  <v-container>
    <v-row>
      <v-btn
        color="green"
        @click="select_galaxies()"
      >select 5 galaxies</v-btn>
    </v-row>
    <v-row>
      <v-col>
        <v-card>
          <c-selection-tool/>
        </v-card>
      </v-col>
      <v-col>
        <v-card>
          <jupyter-widget :widget="widgets.galaxy_table"/>
          <v-card-actions>
            <v-btn @click="story_state.step_index += 1; story_state.step_complete = true">Next Step</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-card>
        <jupyter-widget :widget="viewers.spectrum_viewer"/>
      </v-card>
    </v-row>
  </v-container>
</template>
