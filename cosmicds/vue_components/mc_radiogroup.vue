<template>
  <v-container fluid>
    <v-radio-group
      v-model="column"
      column
    >
      <v-radio
        v-for="[index, option] of radioOptions.entries()"
        :key="index"
        :color="answerKey === index ? colorRight : colorWrong"
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
    <div
      class="text-center"
    >
      <div
        :class="feedbackIndex !== null ? 'd-block' : 'd-none'"
        :color="colors[feedbackIndex]"
      >
        <span :class="answerKey === feedbackIndex ? 'green--text' : 'red--text'">
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
    "answerKey",
    "colors",
    "feedbacks",
    "selectedCallback"
  ],
  data: function () {
    return {
      column: null,
      colorRight: 'green',
      colorWrong: 'red',
      feedbackIndex: null,
    };
  },
  methods: {
    selectChoice: function(index) {
      this.feedbackIndex = index;
      if (this.selectedCallback !== null) {
        this.selectedCallback(index);
      }
    }
  }
};
</script>
