<template>
  <v-card
    flat
    outlined
    class="percentage-selector px-2"
  >
    <v-container
      class="py-0"
    >
      <v-switch
        v-for="(option, index) in options"
        v-model="selected"
        :key="index"
        :value="option"
        :color="radio_color"
        @click.native.stop.prevent="resetIfNeeded(option)"
      >
        <template v-slot:label>
          <span>{{ `${option}%` }}</span>
          <v-dialog content-class="percentage-help-dialog">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                icon
                v-on="on"
                v-bind="attrs"
                @click="selected = option"
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
                  {{ `Inner ${option}% of the data` }}
                </v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <div class="ma-4">
                {{ 
                  `
                  The range of values shown are the inner ${option}% of data points. 
                  This means that ${(100-option)/2}% of the data points in the distribution 
                  have values less than this range, and ${(100-option)/2}% of the data points 
                  have values greater than this range.
                  `
                }}
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

.percentage-help-dialog {
  width: 67% !important;
}

.percentage-selector{
  border: solid 1px black!important;
  background-color: #3a86ff28!important;
  margin-bottom: 0px;
}

.percentage-selector .v-input__slot{
  margin-bottom: 0px!important;
}

.percentage-selector .v-input--selection-controls{
  margin-top: 0px;
  border-top: 0px;
}

.percentage-selector .v-input--selection-controls:first-child{
  margin-top: 14px;
}
</style>
