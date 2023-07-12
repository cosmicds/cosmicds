<template>
  <v-card
    flat
    variant="outlined"
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
        :label="optionText(option)"
      >
    </v-radio-group>
  </v-card>
</template>

<script>
export default {
  methods: {
    optionText(option) {
      if (option === this.selected) {
        return `${option}%: ${this.selected_min} - ${this.selected_max}`;
      } else {
        return `${option}%`;
      }
    }
  }
}
</script>
