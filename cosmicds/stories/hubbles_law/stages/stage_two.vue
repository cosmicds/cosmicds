<template>
  <v-container>
    <v-row class="d-flex align-stretch">
      <v-col
        cols="12"
        lg="4"
      >
        <c-stage-two-start-guidance
          v-if="stage_state.marker == 'two_sta1'" />
      </v-col>
      <v-col
        cols="12"
        lg="8"
      >
        <v-card class="align-self-stretch">
          <c-distance-tool />
        </v-card>
      </v-col>
      <v-col
        cols="12"
        lg="8"
        offset-lg="4"
        v-if="stage_state.distance_sidebar"
      >
        <c-distance-sidebar />
      </v-col>
    </v-row>
    <v-row>
      <v-col
        cols="12"
        lg="4"
      >
        <c-stage-two-holder-alert
          v-if="stage_state.marker == 'two_hol1'" />
      </v-col>
      <v-col
        cols="12"
        lg="8"
      >
        <v-row>
          <v-col
            class="py-0"
          >
            <v-card
              class="align-self-stretch"
              outlined
            >
              <jupyter-widget :widget="widgets.distance_table" />
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="4"
          >
            <!-- FORM DIALOG as template for reflections/MC -->
            <c-angsize-slideshow />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>
