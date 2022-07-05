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
      Angular Size Measurements
    </h3>
    <div
      class="mb-4"
    >
      <p>
        This is the same sky viewer you used earlier to view and choose your galaxies.
      <p>
      </p>
        The vertical line on the left tells you the angular size of the patch of sky being displayed.
      </p>
      <p>
        We have added a new tool that you can use to measure the angular sizes of your galaxies.
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
            state.marker = 'cho_row1'
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
