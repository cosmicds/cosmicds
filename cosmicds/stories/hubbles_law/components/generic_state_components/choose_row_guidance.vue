<template>
  <v-alert
    class="mb-4"
    color="info"
    elevation="6"
  >
    <h3
      class="mb-4"
    >
      Choose a Row
    </h3>
    <div class="mb-4">
      <p>
      Let's take a look at the light spectrum for one of your galaxies.
      </p>
      <p>
      Click on a row in your table to choose that galaxy.
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
      <v-col>
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'sel_gal2';
            state.spectrum_tool_visible = 0;
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </v-alert>
</template>
