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
      <p>
        The <strong>Doppler equation</strong> looks like this:
      </p>
      <v-card
        outlined
        class="legend mt-8"
        color="info"
      >
        <v-container>
          <v-row
            no-gutters
          >
            <v-col>
              <div
                class="JaxEquation"
              >
                $$ v = c \times \left( \frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}} - 1 \right) $$
              </div>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <v-row
            no-gutters
            class="my-1"
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
            class="my-1"
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
            class="my-1"
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
            class="my-1"
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
      </v-card>
    </div>
  </scaffold-alert>
</template>

<style>

.JaxEquation {
  margin: 0;
}

.JaxEquation .MathJax {
  margin: 0 auto 16px !important;
}

.v-application .legend {
  border: 1px solid white !important;
  max-width: 300px;
  margin: 0 auto 0;
  font-size: 15px !important;
}

</style>
