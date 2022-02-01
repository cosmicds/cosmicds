<template>
  <v-container fluid>
    <v-radio-group
      v-model="column"
      column
    >
      <v-radio
        value="radio-1"
        :color="answerKey == 1 ? colorRight : colorWrong"
        @mouseup="oneShow = 1; twoShow = 0; threeShow = 0; fourShow = 0"
      >
        <template v-slot:label>
          <div
            @mouseup="oneShow = 0; twoShow = 1; threeShow = 0; fourShow = 0"
          >
            {{ radioOne }}
          </div>
        </template>
      </v-radio>
      <v-radio
        value="radio-2"
        :color="answerKey == 2 ? colorRight : colorWrong"
        @mouseup="oneShow = 0; twoShow = 1; threeShow = 0; fourShow = 0"
      >
        <template v-slot:label>
          <div
            @mouseup="oneShow = 0; twoShow = 1; threeShow = 0; fourShow = 0"
          >
            {{ radioTwo }}
          </div>
        </template>
      </v-radio>
      <v-radio
        value="radio-3"
        :color="answerKey == 3 ? colorRight : colorWrong"
        @mouseup="oneShow = 0; twoShow = 0; threeShow = 1; fourShow = 0"
      >
        <template v-slot:label>
          <div
            @mouseup="oneShow = 0; twoShow = 0; threeShow = 1; fourShow = 0"
          >
            {{ radioThree }}
          </div>
        </template>
      </v-radio>
      <v-radio
        value="radio-4"
        :color="answerKey == 4 ? colorRight : colorWrong"
        @mouseup="oneShow = 0; twoShow = 0; threeShow = 0; fourShow = 1"
      >
        <template v-slot:label>
          <div
            @mouseup="oneShow = 0; twoShow = 0; threeShow = 0; fourShow = 1"
          >
            {{ radioFour }}
          </div>
        </template>
      </v-radio>
    </v-radio-group>
    <div
      class="text-center"
    >
      <div
        :class="oneShow ? 'd-block' : 'd-none'"
        :color="colorOne"
      >
        <span :class="answerKey == 1 ? 'green--text' : 'red--text'">{{ feedbackOne }}</span>
      </div>
      <div
        :class="twoShow ? 'd-block' : 'd-none'"
        :color="colorTwo"
      >
        <span :class="answerKey == 2 ? 'green--text' : 'red--text'">{{ feedbackTwo }}</span>
      </div>
      <div
        :class="threeShow ? 'd-block' : 'd-none'"
        :color="colorThree"
      >
        <span :class="answerKey == 3 ? 'green--text' : 'red--text'">{{ feedbackThree }}</span>
      </div>
      <div
        :class="fourShow ? 'd-block' : 'd-none'"
        :color="colorFour"
      >
        <span :class="answerKey == 4 ? 'green--text' : 'red--text'">{{ feedbackFour }}</span>
      </div>
    </div>
  </v-container>
</template>

<script>
module.exports = {
  props: ["radioOne","radioTwo","radioThree","radioFour","colorOne","colorTwo","colorThree","colorFour","feedbackOne","feedbackTwo","feedbackThree","feedbackFour","answerKey"],
  data: function () {
    return {
      column: null,
      colorRight: 'green',
      colorWrong: 'red',
      oneShow: 0,
      twoShow: 0,
      threeShow: 0,
      fourShow: 0,
    };
  },
};
</script>