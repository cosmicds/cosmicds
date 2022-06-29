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
      Select Five Galaxies
    </h3>
    <div
      v-if="state.gals_total == 0 & !state.gal_selected"
      class="mb-4"
    >
      <p>
        The green dots in the Cosmic Sky Viewer mark the locations of galaxies you can collect data for. 
      </p>
      <p>
        Pan around the sky and click on one of these dots to select that galaxy.
      </p>
    </div>
    <div
      v-if="state.gals_total < 5 & state.gal_selected"
    >
      <p>
        What do you think of this galaxy?
      </p>
      <p>
        If it looks good to you, click the <v-icon>mdi-plus</v-icon> button to add it to your galaxy collection.
      </p>
      <p>
        If you’d rather look for another galaxy, click the <v-icon>mdi-cached</v-icon> button to reset the view and choose a different green dot.
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
            state.marker = 'sel_gal1'
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      <v-col
        v-if="state.gals_total < 5"
        cols="6"
        class="shrink"
      >
        <div
          style="font-size: 16px;"
        >
          Select {{ 5 - state.gals_total }} <span v-if="state.gals_total > 0">more</span> <span v-if="state.gals_total < 4">galaxies</span><span v-if="state.gals_total == 4">galaxy</span>.
        </div>
      </v-col>
    </v-row>
  </v-alert>
</template>
