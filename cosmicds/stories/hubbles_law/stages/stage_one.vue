<template>
  <v-container>
    <v-row>
      <v-col
        cols="10"
        lg="8"
      >
        <v-row>
          <v-col
            class="py-0"
          >
            <v-card
              :color="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1'] ? 'info' : 'black'"
              :class="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1'] ? 'pa-1 my-n1' : 'pa-0'"
              outlined
            >
              <v-card-title>{{spectrum_name}}</v-card-title>
              <jupyter-widget :widget="viewers.spectrum_viewer"/>

            </v-card>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="2">
        <v-row>
          <v-btn
            icon
            large
            @click="stage_state.galaxy_index = stage_state.galaxy_index - 1"
          >
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <v-btn
            icon
            large
            @click="stage_state.galaxy_index = stage_state.galaxy_index + 1"
          >
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-row>
        <v-row>
          <v-btn
            color="green"
            @click="() => {
              send_spectrum_status({
                name: spectrum_name,
                good: true
              });
              stage_state.galaxy_index = stage_state.galaxy_index + 1
            }"
          >
            Good
          </v-btn>
        </v-row>
        <v-row>
          <v-btn
            color="red"
            @click="() => {
              send_spectrum_status({
                name: spectrum_name,
                good: false
              });
              stage_state.galaxy_index = stage_state.galaxy_index + 1
            }"
          >
            Bad
          </v-btn>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>
