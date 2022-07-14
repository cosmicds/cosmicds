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
      Choose a Row
    </h3>
    <div class="mb-4">
      <p>
      Let's look at the light spectrum for one of your galaxies.
      </p>
      <p>
      Click on a row in your table to choose that galaxy.
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
            state.marker = 'sel_gal3';
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      <v-col
        cols="6"
        class="shrink"
        v-if="!state.spec_viewer_reached"
      >
        <div
          style="font-size: 16px;"
        >
          Select a galaxy from your table.
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="state.spec_viewer_reached"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'mee_spe1';
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
