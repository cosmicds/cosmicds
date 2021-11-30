<template>
  <v-container fluid>
    <v-radio-group
      v-model="column"
      column
    >
      <v-radio
        value="radio-1"
      >
        <template v-slot:label>
          <div>{{ radioOne }}</div>
        </template>
      </v-radio>
      <v-radio
        value="radio-2"
      >
        <template v-slot:label>
          <div>{{ radioTwo }}</div>
        </template>
      </v-radio>
      <v-radio
        value="radio-3"
      >
        <template v-slot:label>
          <div>{{ radioThree }}</div>
        </template>
      </v-radio>
      <v-radio
        value="radio-4"
      >
        <template v-slot:label>
          <div>{{ radioFour }}</div>
        </template>
      </v-radio>
    </v-radio-group>
  </v-container>
</template>

<script>
module.exports = {
  props: ["radioOne","radioTwo","radioThree","radioFour"],
  data: function () {
    return {
      column: null,
    };
  },
};
</script>