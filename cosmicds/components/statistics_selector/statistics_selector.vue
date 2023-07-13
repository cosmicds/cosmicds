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
        :color="color"
        @click.native.stop.prevent="resetIfNeeded(stat)"
      >
        <template v-slot:label>
          <span>{{ capitalizeFirstLetter(stat) }}</span>
          <v-dialog class="help-dialog">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                icon
                v-on="on"
                v-bind="attrs"
              >
                <v-icon small>mdi-help</v-icon>
              </v-btn>
            </template>
            <v-card
              class="mx-auto"
            >
              <v-toolbar
                color="secondary"
                dense
                dark
              >
                <v-toolbar-title
                  class="text-h6 text-uppercase font-weight-regular"
                >
                  {{ stat }}
                </v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <div class="help-content">
                <div class="ma-4">{{ help_text[stat] }}</div>
                <v-img
                  class="my-4 mx-4 image-fit"
                  :src="help_images[stat]"
                  placeholder="https://dummyimage.com/640x360/fff/aaa"
                ></v-img>
              </div>
            </v-card>
          </v-dialog>
        </template>
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

.v-radio .v-input--selection-controls__input,
.v-btn
{
  pointer-events: auto;
}

.help-dialog {
  width: fit-content !important;
}

.help-content {
  display: grid;
  grid-template-rows: 1fr;
  grid-template-columns: 2fr 1fr;
}
</style>
