<template>
  <div class="validation-example-root">
      <div
        v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
      >
        $$ \frac{\input[input-1][input-cls]{}}{\input[input-2][input-cls]{}} $$
      </div>

      <v-btn
        @click="() => {
            const answers = ['input-1', 'input-2'].map(id => parseAnswer(id));
            const expectedAnswers = [state.lambda_rest, state.lambda_obs];
            console.log('expected answers:', expectedAnswers);
            console.log(`Are answers correct? ${
            validateAnswersJS(['input-1', 'input-2'], expectedAnswers)
            }`);
          }"
      >
        Javascript validation
      </v-btn>

      <v-btn
        @click="() => {
          const answers = ['input-1', 'input-2'].map(id => getValue(id));
          validate_python({
            'answers': answers
          })
        }
        "
      >
      Python validation
      </v-btn>
  </div>
</template>

<script>
export default {

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
        return value && value === expectedAnswers[index];
      });
    }
  }

}
</script>