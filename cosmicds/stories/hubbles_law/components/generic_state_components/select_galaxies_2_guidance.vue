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
      v-if="state.gals_total == 0"
      class="mb-4"
    >
      <p>
        The green dots mark the locations of galaxies you can collect data for. 
      </p>
      <p>
        Pan around the sky and click on one of these dots to select that galaxy.
      </p>
    </div>
    <div
      v-if="state.gals_total == 1"
      class="mb-4"
    >
      <p>
        Notice that the table now has a row for your selected galaxy.
      </p>
      <p>
        Now pan around the sky and choose a different galaxy to enter into your table.
      </p>
    </div>
    <div
      v-if="state.gals_total > 1 & state.gals_total < 5"
      class="mb-4"
    >
      <p>
        Check it out, your table is growing.
      </p>
      <p>
        Keep selecting random galaxies until you have 5 rows in your table.
      </p>
    </div>
    <div
      v-if="state.gals_total == 5"
      class="mb-4"
    >
      <p>
        Great, you've got all the galaxies that you need in order to start.
      </p>
      <p>
        Now you can start making measurements from your data.
      </p>
    </div>
    <div
      class="text-center my-8"
    >
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
        cols="4"
        class="shrink"
        v-if="state.gals_total < 5"
      >
        <div
        >
          Select {{ 5 - state.gals_total }} more <span v-if="state.gals_total < 4">galaxies</span><span v-if="state.gals_total == 4">galaxy</span> before moving on.
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="state.gals_total >= 5"
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
