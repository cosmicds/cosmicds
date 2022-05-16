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
    <div
      v-if="complete"
      class="text-right">
      <span class="yellow--text">
        {{ `Score: ${score(tries)} points` }}
      </span>
    </div>

  </v-container>
</template>

<script>
module.exports = {
  props: {
    correctAnswers: Array,
    feedbacks: Array,
    neutralAnswers: Array,
    points: {
      type: [Array, Function],
      default(_rawProps) {
        return function(ntries) { return Math.max(10 - 2 * ntries, 0); };
      }
    },
    radioOptions: Array,
    selectedCallback: Function
  },
  data: function () {
    return {
      column: null,
      colorRight: 'green',
      colorNeutral: 'yellow',
      colorWrong: 'red',
      complete: false,
      feedbackIndex: null,
      tries: 0,
    };
  },
  methods: {
    selectChoice: function(index) {
      this.feedbackIndex = index;
      this.tries += 1;
      if (this.selectedCallback != null) {
        this.selectedCallback(index);
      }
      if (this.correctAnswers.includes(index)) {
        this.complete = true;
      }
    },
    color: function(index) {
      return this.correctAnswers?.includes(index) ? this.colorRight : this.neutralAnswers?.includes(index) ? this.colorNeutral : this.colorWrong;
    },
    score: function(ntries) {
      if (Array.isArray(this.points)) {
        return this.points[ntries-1];
      } else {
        return this.points(ntries);
      }
    }
  }
};
</script>
