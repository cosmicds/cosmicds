<template>
  <v-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
  >
    <h3
      class="mb-4"
      v-if="state.angsizes_total < 5"
    >
      Repeat for Remaining Galaxies
    </h3>
    <h3
      class="mb-4"
      v-if="state.angsizes_total >= 5"
    >
      Nice Work
    </h3>
    <div
      class="mb-4"
      v-if="state.angsizes_total < 5"
    >
      <p>
        Repeat the angular size measurements for each of the remaining galaxies in your table.
      </p>
    </div>
    <div
      class="mb-4"
      v-if="state.angsizes_total >= 5"
    >
      <p>
        You have measured the angular size for all of your galaxies.
      </p>
      <p>
        You can continue to refine your measurements, or, if you are satisfied with your measurements, you can move on.
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
            state.marker = 'ang_siz6'
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      <v-col
        v-if="state.angsizes_total < 5"
        cols="6"
        class="shrink"
      >
        <div
          style="font-size: 16px;"
        >
          Measure wavelength<span v-if="state.angsizes_total < 4">s</span> for {{ 5 - state.angsizes_total }} more <span v-if="state.angsizes_total < 4">galaxies</span><span v-if="state.angsizes_total == 4">galaxy</span>.
        </div>
      </v-col>
      <v-col
        v-if="state.angsizes_total >= 5"
        class="shrink"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'est_dis1'
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
