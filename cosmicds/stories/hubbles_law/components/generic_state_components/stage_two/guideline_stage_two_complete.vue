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
      Distances Complete
    </h3>
    <div
      class="mb-4"
    >
      <p>
        You are ready to move on to the next stage.
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
      <v-col
        class="shrink"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'fil_rem1'
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </v-alert>
</template>
