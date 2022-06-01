<template>
  <v-container
    fluid
    class="px-8"
  >
    <v-radio-group
      v-model="column"
      column
    >
      <v-radio
        v-for="[index, option] of radioOptions.entries()"
        :key="index"
        :color="`${color(index)} lighten-1`"
        @mouseup="selectChoice(index)"
      >
        <template v-slot:label>
          <div
            @mouseup="selectChoice(index)"
          >
            {{ option }}
          </div>
        </template>
      </v-radio>
    </v-radio-group>
    <v-alert
      dense
      :color="`${color(feedbackIndex)} lighten-4`"
      :class="feedbackIndex !== null ? 'd-block' : 'd-none'"
    >
      <span
        :class="`${color(feedbackIndex)}--text text--darken-4`"
      >
        {{ feedbacks[feedbackIndex] }}
      </span>
    </v-alert>
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
      colorNeutral: 'orange',
      colorWrong: 'red',
      feedbackIndex: null,
    };
  },
  methods: {
    selectChoice: function(index) {
      this.feedbackIndex = index;
      if (this.selectedCallback != null) {
        this.selectedCallback(index);
      }
    },
    color: function(index) {
      return this.correctAnswers?.includes(index) ? this.colorRight : this.neutralAnswers?.includes(index) ? this.colorNeutral : this.colorWrong;
    }
  }
};
</script>