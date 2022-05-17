<template>
  <scaffold-alert
    header-text="The Doppler Equation"
    @back="
      state.marker = 'dop_cal1';
    "
    @next="
      state.marker = 'dop_cal3';
    "
  >
    <div
      class="mb-4"
    >
      <v-container>
        <v-row
          no-gutters
        >
          <v-col>
            The <strong>Doppler equation</strong> looks like this:
          </v-col>
        </v-row>
        <v-row>
          <v-col
            class="JaxEquation"
          >
            $$ v=c \left(\frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}}-1\right) $$
          </v-col>
        </v-row>
        <v-row
          no-gutters
          class="my-1 legend-text"
        >
          <v-col
            
          >
            \(v\)
          </v-col>
          <v-col
            cols="10"
          >
            velocity of your galaxy, in km/s
          </v-col>
        </v-row>
        <v-row
          no-gutters
          class="my-1 legend-text"
        >
          <v-col
            cols="2"
          >
            \(c\)
          </v-col>
          <v-col
            cols="10"
          >
            speed of light, 300,000 km/s
          </v-col>
        </v-row>
        <v-row
          no-gutters
          class="my-1 legend-text"
        >
          <v-col
            cols="2"
          >
            \(\lambda_{\text{obs}}\)
          </v-col>
          <v-col
            cols="10"
          >
            observed wavelength of spectral line in your galaxy
          </v-col>
        </v-row>
        <v-row
          no-gutters
          class="my-1 legend-text"
        >
          <v-col
            cols="2"
          >
            \(\lambda_{\text{rest}}\)
          </v-col>
          <v-col
            cols="10"
          >
            rest wavelength of spectral line
          </v-col>
        </v-row>
      </v-container>
    </div>
  </scaffold-alert>
</template>

<style>

.JaxEquation .MathJax {
  margin: 0 auto 0 !important;
}

.legend-text {
  font-size: 16px !important;
}

</style>
