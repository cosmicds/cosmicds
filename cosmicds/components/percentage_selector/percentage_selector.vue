<template>
  <v-card
    flat
    light
    variant="outlined"
    color="white"
    class="percentage-selector"
  >
    <v-radio-group
      v-model="selected"
      column
    >
      <v-radio
        v-for="(option, index) in options"
        :key="index"
        :value="option"
      >
    </v-radio-group>
  </v-card>
</template>

<script>
export default {
  props: {
    options: {
      validator(value) {
        return Array.isArray(value) && value.every(x => typeof x === "number");
      },
      required: true
    }
  } 
}
</script>

<style scoped>
.v-card {
  border: solid 1px black !important;
}
</style>
