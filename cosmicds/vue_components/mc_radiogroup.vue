<template>
  <v-container fluid>
    <v-radio-group
      v-model="column"
      column
      :disabled='complete'
    >
      <v-radio
        v-for="[index, option] of radioOptions.entries()"
        :key="index"
        :color="color(index)"
        @change="selectChoice(index)"
      >
        <template v-slot:label>
          <div>
          {{ option }}
          </div>
        </template>
      </v-radio>
    </v-radio-group>
    <div
      class="text-center"
    >
      <div
        :class="feedbackIndex !== null ? 'd-block' : 'd-none'"
      >
        <span :class="`${color(feedbackIndex)}--text`">
          {{ feedbacks[feedbackIndex] }}
        </span>
      </div>
    </div>
  </v-container>
</template>

<script>
module.exports = {
  props: [
    "radioOptions",
    "correctAnswers",
    "neutralAnswers",
    "feedbacks",
    "selectedCallback"
  ],
  data: function () {
    return {
      column: null,
      colorRight: 'green',
      colorNeutral: 'yellow',
      colorWrong: 'red',
      complete: false,
      feedbackIndex: null,
    };
  },
  methods: {
    selectChoice: function(index) {
      this.feedbackIndex = index;
      if (this.selectedCallback != null) {
        this.selectedCallback(index);
      }
      if (this.correctAnswers.includes(index)) {
        this.complete = true;
      }
    },
    color: function(index) {
      return this.correctAnswers?.includes(index) ? this.colorRight : this.neutralAnswers?.includes(index) ? this.colorNeutral : this.colorWrong;
    }
  }
};
</script>
