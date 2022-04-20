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
        $$ \text{ }= c \left(\frac{\bbox[DarkSlateGrey]{\input[lam_obs][]{}}}{\bbox[DarkSlateGrey]{\input[lam_rest][]{}}}-1\right)  $$
      </p>
      Remember:
      <p>      
        \(v\): velocity of your galaxy, in km/s <br>
        \(c\): speed of light, 300,000 km/s <br>
        \(\lambda_{\text{obs}}\): observed wavelength of spectral line in your galaxy <br>
        \(\lambda_{\text{rest}}\): rest wavelength of spectral line} <br>
      </p>
    </div>
    <v-divider
      class="my-4"
    >
    </v-divider>

      <div
        v-if="failedValidation"
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
          v-if="!failedValidation"
          class="black--text"
          color="accent"
          elevation="2"
          @click="() => {
            const answers = ['lam_obs', 'lam_rest'].map(id => parseAnswer(id));
            const expectedAnswers = [state.lambda_obs, state.lambda_rest];
            validateAnswersJS(['lam_obs', 'lam_rest'], expectedAnswers) ? state.marker = 'dop_cal2' : 'dop_cal4';
            console.log(this)
            console.log('expected answers:', expectedAnswers);
            console.log(`Are answers correct? ${
            validateAnswersJS(['lam_obs', 'lam_rest'], expectedAnswers)
            }`);
          }"
        >
          next
        </v-btn>
        <v-btn
          v-if="failedValidation"
          class="black--text"
          color="accent"
          elevation="2"
          @click="() => {
            const answers = ['lam_obs', 'lam_rest'].map(id => parseAnswer(id));
            const expectedAnswers = [state.lambda_obs, state.lambda_rest];
            validateAnswersJS(['lam_obs', 'lam_rest'], expectedAnswers) ? state.marker = 'dop_cal2' : 'dop_cal4';
            console.log(this)
            console.log('expected answers:', expectedAnswers);
            console.log(`Are answers correct? ${
            validateAnswersJS(['lam_obs', 'lam_rest'], expectedAnswers)
            }`);
          }"
        >
          try again
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
      return parseFloat(this.getValue(inputID));
    },

    validateAnswersJS(inputIDs, expectedAnswers) {
      console.log("We're validating with Javascript!");
      return inputIDs.every((id, index) => {
        const value = this.parseAnswer(id);
        this.failedValidation = (value && value === expectedAnswers[index]) ? false : true;
        console.log("Did validation fail", this.failedValidation);
        return value && value === expectedAnswers[index];
      });
    }
  },
};
  // <scaffold-alert
  //   header-text="Velocity Calculation"
  //   @back="
  //     state.marker = 'dop_cal3';
  //   "
  //   @next="
  //     state.marker = 'dop_cal4';
  //   "
  // >
  //           "
  //           state.marker = 'dop_cal2'; //just to check for now that it goes somewhere when correct
  //         "
</script>

