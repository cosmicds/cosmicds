<template>
  <v-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
  >
    <h3
      class="mb-4"
    >
      Select Five Galaxies
    </h3>
    <div
      class="mb-4"
    >
      <p>
        This is a view of the cosmic sky, like the one you explored in the introduction. This view shows a more modern data set from the Sloan Digital Sky Survey (SDSS), which has collected imaging and spectral data for millions of galaxies. 
      </p>
      <p>
        This Data Story will focus on a nearby subset of galaxies.
      </p>
    </div>
    
    <v-divider
      class="my-4"
    >
    </v-divider>

    <v-row
      align="center"
      no-gutters
    >
      <v-col>
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'mee_gui1'
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      <v-col
        v-if="state.gals_total == 0"
        class="shrink"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'sel_gal2'
          "
        >
          next
        </v-btn>
      </v-col>
      <v-col
        v-if="state.gals_total > 0"
        class="shrink"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'sel_gal3'
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>