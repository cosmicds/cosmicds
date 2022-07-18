<template>
  <v-container
    fluid
    class="px-8"
  >
    <v-radio-group
      v-model="column"
      column
      :disabled='complete'
    >
      <v-radio
        v-for="[index, option] of radioOptions.entries()"
        :key="index"
        :color="`${color(index)} lighten-1`"
        @change="selectChoice(index)"
      >
        <template v-slot:label>
          <div>
          {{ option }}
          </div>
        </template>
      </v-radio>
    </v-radio-group>
    <v-alert
      v-show="feedbackIndex !== null"
      outlined
      :color="`${color(feedbackIndex)}`"
      :type="complete ? 'success' : 'warning'"
    >
      <div
        v-html="feedbacks[feedbackIndex]"
      >
      </div>
      <div
        v-if="scoring && complete"
        class="text-right"
      >
        <strong>{{ `+ ${score} ${score == 1 ? 'point' : 'points'}` }}</strong>
        <v-icon
          class="ml-1"
          :color="`${color(feedbackIndex)}`"
        >
          mdi-piggy-bank
        </v-icon>
      </div>
    </v-alert>
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
    scoring: {
      type: Boolean,
      default: true
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
      colorNeutral: 'orange',
      colorWrong: 'red',
      complete: false,
      feedbackIndex: null,
      tries: 0,
      score: 0
    };
  },
  methods: {
    selectChoice: function(index) {
      this.feedbackIndex = index;
      this.tries += 1;
      const correct = this.correctAnswers.includes(index);
      if (correct) {
        this.complete = true;
        if (this.scoring) {
          this.score = this.getScore(this.tries);
        }
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
      if (this.correctAnswers.includes(index)) {
        return this.colorRight;
      } else if (this.neutralAnswers.includes(index)) {
        return this.colorNeutral;
      } else {
        return this.colorWrong;
      }
    },
    getScore: function(ntries) {
      if (Array.isArray(this.points)) {
        return ntries <= this.points.length ? this.points[ntries-1] : 0;
      } else {
        return this.points(ntries);
      }
    }
  }
};
</script>
