<template>
  <v-alert
    class="mb-4"
    color="info"
    elevation="6"
  >
    <h3
      class="mb-4"
    >
      Input Spectral Line Wavelengths
    </h3> 

    <div
      class="mb-4"
      v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
    >
      <p>
        Enter the observed and rest wavelengths of the spectral line for your chosen galaxy into the cells in the equation below.
      </p>
      <p>
        $$ v=c \left(\frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}}-1\right) $$ 
        $$ \text{ }= c \left(\frac{\bbox[DarkSlateGrey]{\input[lam_obs][]{}} \text{ &#8491;}}{\bbox[DarkSlateGrey]{\input[lam_rest][]{}}\text{ &#8491;}}-1\right)  $$
      </p>
      <div class="text-caption">
        <p>
          Remember:
        </p>
        <p>      
          \(v\): velocity of your galaxy, in km/s <br>
          \(c\): speed of light, 300,000 km/s <br>
          \(\lambda_{\text{obs}}\): observed wavelength of spectral line in your galaxy <br>
          \(\lambda_{\text{rest}}\): rest wavelength of spectral line} <br>
        </p>
      </div>
    </div>
    <v-divider
      class="my-4"
      v-if="failedValidation4"
    >
    </v-divider>

      <div
        v-if="failedValidation4"
      >
          Not quite. Make sure you haven't reversed the rest and observed wavelength values.
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
            const answers = ['lam_obs', 'lam_rest'].map(id => parseAnswer(id));
            const expectedAnswers = [state.lambda_obs, state.lambda_rest];
            state.marker = validateAnswersJS(['lam_obs', 'lam_rest'], expectedAnswers) ? 'dop_cal5' : 'dop_cal4';
            state.doppler_calc_dialog = validateAnswersJS(['lam_obs', 'lam_rest'], expectedAnswers) ? true: false;
            console.log('dialog');
            console.log(state.doppler_calc_dialog, state.marker);          
          }"
        >
          {{ (!failedValidation4 ) ? 'next' : 'try again' }}
        </v-btn>
      </v-col>

    </v-row>

  </v-alert>
</template>


<script>
export default = {

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

