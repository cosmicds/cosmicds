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
      Select a Galaxy
    </h3>
    <div class="mb-4">
      <p>
        Click on a row in your table to select one of the galaxies.
      </p>
      <p>
        You will calculate the velocity for this galaxy using the Doppler equation.
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
            state.marker = 'dop_cal2';
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      <v-col
        cols="6"
        class="shrink"
        v-if="!state.doppler_calc_reached"
      >
        <div
          style="font-size: 16px;"
        >
          Select a galaxy from your table.
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="state.doppler_calc_reached"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'dop_cal4';
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>


<style>

.JaxEquation .MathJax {
  margin: 0 auto 16px !important;
}

</style>