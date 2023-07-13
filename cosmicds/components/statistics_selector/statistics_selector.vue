<template>
  <v-card
    flat
    variant="outlined"
    class="statistics-selector"
  >
    <v-radio-group
      v-model="selected"
      column
    >
      <v-radio
        v-for="(stat, index) in statistics"
        :key="index"
        :value="stat"
        :label="capitalizeFirstLetter(stat)"
        :color="color"
        @click.native.stop.prevent="resetIfNeeded(stat)"
      >
      </v-radio>
    </v-radio-group>
  </v-card>
</template>

<script>
export default {
  methods: {
    capitalizeFirstLetter(text) {
      return text.charAt(0).toUpperCase() + text.slice(1);
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
