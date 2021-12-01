<template>
  <v-stepper-step :complete="state.step > 1" step="1">
    Estimate Age of Universe
  </v-stepper-step>

  <v-stepper-content step="1">
    <v-skeleton-loader
      class="mb-6"
      boilerplate
      type="article"
    ></v-skeleton-loader>
    <v-btn color="primary" @click="state.step = 0"> Continue </v-btn>
    <v-btn text> Cancel </v-btn>
  </v-stepper-content>
</template>