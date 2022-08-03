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
      Time to Explore Your Data
    </h3>
    <div
      class="mb-4"
    >
      <p>
        Now, you have a table of velocity and distance data for your galaxies, like Hubble did.
      <p>
      </p>
        Hubble graphed his data with velocity on the y-axis and distance on the x-axis. Let’s do the same with your data and see what it looks like.
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
      <v-spacer></v-spacer>
      <v-col
        class="shrink"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'ran_mar2'
          "
        >
          graph
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
