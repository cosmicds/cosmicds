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
      Observed Wavelength
    </h3>
    <div
      class="mb-4"
    >
      <p>
        Hover your mouse in the Spectrum Viewer. A vertical measuring tool identifies the wavelength as you move the tool left and right.
      </p>
      <p>
        Align the measuring tool to the <strong>{{ state.element }} (observed)</strong> marker and click. This records the <strong>observed wavelength</strong> in your table.
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
            state.marker = 'res_wav1';
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      
      <v-col
        cols="6"
        class="shrink"
        v-if="state.obswaves_total < 1"
      >
        <div
          style="font-size: 16px;"
        >
          Measure the observed wavelength.
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="state.obswaves_total >= 1"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'obs_wav2';
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
