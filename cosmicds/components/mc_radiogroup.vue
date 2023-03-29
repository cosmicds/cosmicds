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
      v-show="column !== null"
      outlined
      :color="`${color(column)}`"
      :icon="`${icon(column)}`"
    >
      <div
        v-html="feedbacks[column]"
        class="feedback"
      >
      </div>
      <div
        v-if="scoring && complete"
        class="text-right"
      >
        <strong>{{ `+ ${score} ${score == 1 ? 'point' : 'points'}` }}</strong>
        <v-icon
          large
          class="ml-1"
          :color="`${color(column)}`"
        >
          mdi-piggy-bank
        </v-icon>
      </div>
    </v-alert>
  </v-container>
</template>

<style scoped>

.feedback{
  color: white;
}

</style>

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
    scoreTag: String,
  },
  emits: {
    select(status) {
      return typeof status.index === 'number' &&
             typeof status.correct === 'boolean' &&
             typeof status.neutral === 'boolean' &&
             typeof status.tries === 'number';
    }
  },
  created() {
    if (!this.scoreTag) { return; }
    document.addEventListener("mc-initialize-response", this.onInitResponse);
    document.dispatchEvent(
      new CustomEvent("mc-initialize", {
        detail: {
          tag: this.scoreTag
        }
      })
    );
  },
  data: function () {
    return {
      column: null,
      colorRight: 'green',
      colorNeutral: 'orange',
      colorWrong: 'red',
      iconRight: 'mdi-check-circle-outline',
      iconNeutral: 'mdi-lightbulb-on-outline',
      iconWrong: 'mdi-alert-circle-outline',
      complete: false,
      tries: 0,
      score: null
    };
  },
  methods: {
    selectChoice: function(index, send=true) {
      this.column = index;
      this.tries += 1;
      const correct = this.correctAnswers.includes(index);
      const neutral = this.neutralAnswers.includes(index);
      this.complete = correct || (this.correctAnswers.length === 0 && neutral);
      this.score = (this.scoring && this.complete) ? this.getScore(this.tries) : null;
      if (this.scoreTag !== undefined && send) {
        document.dispatchEvent(
          new CustomEvent("mc-score", {
            detail: {
              tag: this.scoreTag,
              score: this.score,
              choice: this.column,
              tries: this.tries
            }
          })
        );
      }
      this.$emit('select', {
        index: index,
        correct: correct,
        neutral: this.neutralAnswers.includes(index),
        tries: this.tries
      });
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
    icon: function(index) {
      if (this.correctAnswers.includes(index)) {
        return this.iconRight;
      } else if (this.neutralAnswers.includes(index)) {
        return this.iconNeutral;
      } else {
        return this.iconWrong;
      }
    },
    getScore: function(ntries) {
      if (Array.isArray(this.points)) {
        return ntries <= this.points.length ? this.points[ntries-1] : 0;
      } else {
        return this.points(ntries);
      }
    },
    onInitResponse(event) {
      const data = event.detail;
      if (data.tag !== this.scoreTag) { return; }
      if (data.found) {
        this.tries = data.tries - 1; // selectChoice adds a try
        this.selectChoice(data.choice, false); // no need to tell the state what it just told us
      }
      document.removeEventListener("mc-initialize-response", this.onInitResponse);
    }
  }
};
</script>
