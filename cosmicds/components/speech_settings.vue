<template>
  <v-card min-width="300">
    <v-list>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Speech Reader</v-list-item-title>
          <v-list-item-subtitle>Adjust speech settings</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item>
        <v-slider
          v-model="state.speech_rate"
          label="Rate"
          color="blue"
          :min="0.5"
          :max="2"
          :step="0.1"
          thumb-label
        >
        </v-slider>
      </v-list-item>
      <v-list-item>
        <v-slider
          v-model="state.speech_pitch"
          label="Pitch"
          color="blue"
          :min="0.1"
          :max="2"
          :step="0.1"
          thumb-label
        >
        </v-slider>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
module.exports = {
  props: ['state']
}
</script>
