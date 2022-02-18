<template>
  <v-container>
    <p> This is a test</p>
    <v-row>
      <v-col>
        <v-card>
          <jupyter-widget :widget="widgets.wwt_viewer"/>
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
  </v-container>
</template>