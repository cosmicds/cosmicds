<template>
  <v-stepper v-model="state.tab">
    <v-stepper-items>
      <v-stepper-content v-for="(step, key, i) in state.steps" :step="i" :key="key">
        <!-- <v-card>
          <jupyter-widget :widget="viewers.wwt_viewer"></jupyter-widget>
        </v-card> -->
        <v-card class="mb-12" color="grey lighten-1" height="200px"></v-card>
        
        <v-btn color="primary" @click="state.tab = i < Object.keys(state.steps).length - 1 ? i + 1 : 0"> Continue </v-btn>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>