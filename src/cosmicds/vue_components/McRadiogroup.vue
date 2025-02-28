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
        :color="`${color(index)}`"
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
        v-if="scoring && complete && score > 0"
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
  color: #EEEEEE;
}
.v-alert {
  background-color: #000D!important;
}

</style>

<script>
module.exports = {
  
  props: {
    initialization: {
      type: Object,
      default: () => undefined
    },
    feedbacks: Array,
    correctAnswers: {
      type: Array,
      default: () => []
    },
    scoring: {
      type: Boolean,
      default: true
    },
    neutralAnswers: {
      type: Array,
      default: () => []
    },
    points: {
      type: [Array, Function],
      default(_rawProps) {
        return function(nwrong) { return Math.max(10 - 2 * nwrong, 0); };
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
    },
  },
  created() {
    if (!this.scoreTag) { return; }
    this.$emit("mc-emit",['mc-initialize-response', this.scoreTag]);
  },
  
  mounted() {    
    
    if (this.initialization) {
      if (this.initialization.tag !== this.scoreTag) { return; }
      this.tries = this.initialization.tries ?? this.tries;
      this.wrongAttempts = this.initialization.wrong_attempts ?? this.wrongAttempts;
      if (this.initialization.choice !== undefined) {
        this.selectChoice(this.initialization.choice, true);  // No need to update counts and send message for initialization
      }
    }
  },
  data: function () {
    return {
      column: null,
      colorRight: '#00E676',
      colorNeutral: 'white',
      colorWrong: 'red',
      iconRight: 'mdi-check-circle-outline',
      iconNeutral: 'mdi-lightbulb-on-outline',
      iconWrong: 'mdi-alert-circle-outline',
      complete: false,
      tries: 0,
      score: null,
      wrongAttempts: 0
    };
  },
  methods: {
    selectChoice: function(index, forInitialization=false) {
      this.column = index;
      const correct = this.correctAnswers.includes(index);
      const neutral = this.neutralAnswers.includes(index);
      const wrong = !(correct || neutral);
      if (!forInitialization) {
        this.tries += 1;
        if (wrong) {
          this.wrongAttempts += 1;
        }
      }
      this.complete = correct || (this.correctAnswers.length === 0 && neutral);
      if (this.scoring && this.complete) {
        this.score = this.getScore(this.wrongAttempts);
      }
      if (this.scoreTag !== undefined && !forInitialization) {
        this.$emit("mc-emit", ["mc-score", {
          tag: this.scoreTag,
          score: this.score,
          choice: this.column,
          tries: this.tries,
          wrong_attempts: this.wrongAttempts
        }]);
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
    getScore: function(nwrong) {
      if (Array.isArray(this.points)) {
        return nwrong <= this.points.length ? this.points[nwrong-1] : 0;
      } else {
        return this.points(nwrong);
      }
    },
  }
};
</script>
