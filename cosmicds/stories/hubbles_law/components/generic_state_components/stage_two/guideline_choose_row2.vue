<template>
  <v-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
  >
    <h3
      class="mb-4"
    >
      Choose a Galaxy
    </h3>
    <div
      class="mb-4"
    >
      <p>
        Click on a row to choose a galaxy whose distance we will estimate.
      </p>
    </div>
    
    <v-divider
      class="my-4"
    >
    </v-divider>

    <v-row
      align="center"
      no-gutters
    >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'est_dis2'
          "
        >
          back
        </v-btn>
      <v-spacer></v-spacer>
      <v-col
        cols="6"
        class="shrink"
        v-if="!state.galaxy_selected"
      >
        <div
          style="font-size: 16px;"
        >
          Select a galaxy from your table.
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="state.galaxy_selected"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'est_dis3'
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
