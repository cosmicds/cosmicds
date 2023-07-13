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
        :label="`${option}%`"
        :color="radio_color"
        @click.native.stop.prevent="resetIfNeeded(option)"
      >
      </v-radio>
    </v-radio-group>
  </v-card>
</template>

<script>
export default {
  methods: {
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
