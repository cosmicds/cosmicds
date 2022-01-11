<template>
  <v-footer color="secondary" bottom padless style="border-radius: 3px">
    <v-row justify="center" no-gutters>
      <v-btn color="white" text rounded class="my-2"> Home </v-btn>
      <v-btn color="white" text rounded class="my-2"> About Us </v-btn>
      <v-btn color="white" text rounded class="my-2"> Team </v-btn>
      <v-btn color="white" text rounded class="my-2"> Contact Us </v-btn>
      <v-col
        class="primary py-4 text-center white--text"
        cols="12"
        style="border-radius: 3px"
      >
        {{ new Date().getFullYear() }} — <strong>CosmicDS Project</strong>
      </v-col>
    </v-row>
  </v-footer>
</template>