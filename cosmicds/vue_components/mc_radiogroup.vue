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
        <span
          :class="`${color(feedbackIndex)}--text`" 
          v-html="feedbacks[feedbackIndex]"
        >
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
    feedbacks: Array,
    correctAnswers: {
      type: Array,
      default: []
    },
    neutralAnswers: {
      type: Array,
      default: []
    },
    points: {
      type: [Array, Function],
      default(_rawProps) {
        return function(ntries) { return Math.max(12 - 2 * ntries, 0); };
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
      const correct = this.correctAnswers.includes(index);
      if (correct) {
        this.complete = true;
      }
      if (this.selectedCallback != null) {
        this.selectedCallback({
          index: index,
          correct: correct,
          neutral: this.neutralAnswers.includes(index),
          tries: this.tries
        });
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
