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
        :color="color"
        @click.native.stop.prevent="resetIfNeeded(option)"
      >
      </v-radio>
    </v-radio-group>
  </v-card>
</template>

<script>
export default {
  methods: {
    optionText(option) {
      const unitStr = this.unit ? ` ${this.unit}` : "";
      if (option === this.selected) {
        return `${option}%: ${this.selected_min}${unitStr} - ${this.selected_max}${unitStr}`;
      } else {
        return `${option}%`;
      }
    },
    resetIfNeeded(value) {
      this.was_selected = (this.was_selected === value) ? null : value;
      this.selected = this.was_selected;
    }
  }
}
</script>

<style scoped>
.v-radio {
  pointer-events: none;
}

.v-radio .v-input--selection-controls__input {
  pointer-events: auto;
}
</style>
