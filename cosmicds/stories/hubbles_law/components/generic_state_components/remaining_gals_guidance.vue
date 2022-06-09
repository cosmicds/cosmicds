<template>
  <v-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
  >
    <h3
      class="mb-4"
      v-if="state.obswaves_total < 5"
    >
      Repeat for Remaining Galaxies
    </h3>
    <h3
      class="mb-4"
      v-if="state.obswaves_total >= 5"
    >
      Nice Work
    </h3>
    <div
      class="mb-4"
      v-if="state.obswaves_total < 5"
    >
      <p>
        Your measurement of the line’s observed wavelength is now recorded in the table for your selected galaxy.
      </p>
      <p>
        Go through each of the remaining galaxies in your table and repeat these measurements, until you have recorded rest and observed wavelengths for each of your galaxies.
      </p>
    </div>
    <div
      class="mb-4"
      v-if="state.obswaves_total >= 5"
    >
      <p>
        You have measured the spectral line wavelengths for all of your galaxies.
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
            state.marker = 'obs_wav2'
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      <v-col
        v-if="state.obswaves_total < 5"
        cols="6"
        class="shrink"
      >
        <div
          style="font-size: 16px;"
        >
          Measure wavelength<span v-if="state.obswaves_total < 4">s</span> for {{ 5 - state.obswaves_total }} more <span v-if="state.obswaves_total < 4">galaxies</span><span v-if="state.obswaves_total == 4">galaxy</span>.
        </div>
      </v-col>
      <v-col
        v-if="state.obswaves_total >= 5"
        class="shrink"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'ref_dat1'
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
