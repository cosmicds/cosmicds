<template>
  <v-alert
    color="info"
    class="mb-4 mx-auto doppler_alert"
    max-width="800"
    elevation="6"
  >
    <h3
      class="mb-4"
    >
      Input Wavelengths
    </h3> 

    <div
      class="mb-4"
      v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
    >
      <p>
        Enter the observed wavelength and rest wavelength for your chosen galaxy into the cells in the equation below.
      </p>
      <div
        class="JaxEquation my-8"
      >
        $$ v = c \times \left( \frac{\bbox[#FBE9E7]{\input[lam_obs][]{}} \text{ &#8491;}}{\bbox[#FBE9E7]{\input[lam_rest][]{}}\text{ &#8491;}} - 1 \right) $$
      </div>
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
    <v-divider
      class="my-4"
      v-if="failedValidation4"
    >
    </v-divider>
      <v-alert
        v-if="failedValidation4"
        dense
        color="info darken-1"
      >
        Not quite. Make sure you haven't reversed the rest and observed wavelength values.
      </v-alert>
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
            state.marker = 'dop_cal3';
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      <v-col
        class="shrink"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="() => {
            const expectedAnswers = [state.lambda_obs, state.lambda_rest];
            state.marker = validateAnswersJS(['lam_obs', 'lam_rest'], expectedAnswers) ? 'dop_cal5' : 'dop_cal4';
            state.doppler_calc_dialog = validateAnswersJS(['lam_obs', 'lam_rest'], expectedAnswers) ? true: false;   
          }"
        >
          next
        </v-btn>
      </v-col>

    </v-row>

  </v-alert>
</template>


<style>

.JaxEquation .MathJax {
  margin: 16px auto !important;
}

mjx-mfrac {
  margin: 0 4px !important;
}

mjx-mstyle {
  border-radius: 5px;
}

.doppler_alert .v-alert {
  font-size: 16px !important;
}

.v-application .legend {
  border: 1px solid white !important;
  max-width: 300px;
  margin: 0 auto 0;
  font-size: 15px !important;
}

#lam_obs, #lam_rest {
  color:  black;
  font-size: 18px;
  font-family: "Roboto", Arial, Helvetica, sans-serif;
  padding: 3px;
}

</style>


<script>
export default {

    methods: {
    getValue(inputID) {
      const input = document.getElementById(inputID);
      if (!input) { return null; }
      return input.value;
    },

    parseAnswer(inputID) {
      return parseFloat(this.getValue(inputID).replace(/,/g,''));
    },

    validateAnswersJS(inputIDs, expectedAnswers) {
      return inputIDs.every((id, index) => {
        const value = this.parseAnswer(id);
        this.failedValidation4 = (value && value === expectedAnswers[index]) ? false : true;
        return value && value === expectedAnswers[index];
      });
    }
  },
};
</script>

