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
      Angular Size Measurement
    </h3>
    <div
      class="mb-4"
    >
      <p>
        Click on one edge of your galaxy to mark the ruler's starting point.
      </p>
      <p>
        With the button held down, drag to the other edge of your galaxy and release the button.
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
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'ang_siz3'
          "
        >
          back
        </v-btn>
      <v-spacer></v-spacer>
      <v-col
        cols="6"
        class="shrink"
        v-if="state.n_meas==0"
      >
        <div
          style="font-size: 16px;"
        >
          Measure angular size of galaxy
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="state.n_meas>0"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'ang_siz5'
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
