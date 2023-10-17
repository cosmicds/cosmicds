<template>
  <v-card
    flat
    outlined
    class="statistics-selector px-2"
  >
    <v-container
      class="py-0"
    >
      <v-switch
        v-for="(stat, index) in statistics"
        v-model="selected"
        :key="index"
        :value="stat"
        :color="color"
        @click.native.stop.prevent="resetIfNeeded(stat)"
      >
        <template v-slot:label>
          <span>{{ capitalizeFirstLetter(stat) }}</span>
          <v-dialog content-class="stat-help-dialog">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                icon
                v-on="on"
                v-bind="attrs"
                @click="selected = stat"
              >
                <v-icon medium>mdi-help-circle-outline</v-icon>
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
              <div class="stat-help-content">
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
      </v-switch>
    </v-container>
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

.stat-help-dialog {
  width: fit-content !important;
}

.stat-help-content {
  display: grid;
  grid-template-rows: 1fr;
  grid-template-columns: 2fr 1fr;
}

.statistics-selector.theme--light.v-card.v-card--outlined {
  border: solid 1px grey!important;
  background-color: #e0e9fc!important;
  margin-bottom: 0px;
}

.statistics-selector .theme--light.v-label {
    color: black !important;
}

.statistics-selector.theme--dark.v-card.v-card--outlined {
  border: solid 1px grey!important;
  background-color: #233149!important;
  margin-bottom: 0px;
}

.statistics-selector .theme--dark.v-label {
    color: white !important;
}

.statistics-selector .v-input__slot{
  margin-bottom: 0px!important;
}

.statistics-selector .v-input--selection-controls{
  margin-top: 0px;
  border-top: 0px;
}

.statistics-selector .v-input--selection-controls:first-child{
  margin-top: 14px;
}
</style>
