<template>
  <v-alert
    :class="state.marker == 'sel_gal1' ? 'd-block' : 'd-none'"
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
      :class="state.gals_total == 0 ? 'd-block' : 'd-none'"
      class="mb-4"
    >
      <p>
        This is another view of the night sky, similar to the one you explored earlier. This view shows a more modern data set from the Sloan Digital Sky Survey (SDSS), which has collected imaging and spectral data for millions of galaxies. This Data Story will focus on a nearby subset of galaxies.
      </p>
      <p>
        The <strong :class="state.darkmode ? 'green--text text--lighten-3' : 'green--text text--darken-2'">green</strong> dots mark the locations of galaxies you can collect data for. 
      </p>
      <p>
        Pan around the sky and click on one of these dots to select that galaxy.
      </p>
    </div>
    <div
      :class="state.gals_total == 1 ? 'd-block' : 'd-none'"
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
      :class="state.gals_total > 1 & state.gals_total < 5 ? 'd-block' : 'd-none'"
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
      :class="state.gals_total == 5 ? 'd-block' : 'd-none'"
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
    <div
      class="mb-2 mx-4"
    >
      <v-row
        no-gutters
        class="mb-3"
      >
        <v-col
          cols="3"
        >
          <strong>Pan</strong>
        </v-col>
        <v-col
          cols="9"
        >
          <strong>click + drag</strong><br>
          (or use the <strong class="codeFont">I-J-K-L</strong> keys)
        </v-col>
      </v-row>
      <v-row
        no-gutters
      >
        <v-col
          cols="3"
        >
          <strong>Zoom</strong>
        </v-col>
        <v-col
          cols="9"
        >
          <strong>scroll in and out</strong><br>
          (or use the <strong class="codeFont">Z-X</strong> keys for finer zoom)
        </v-col>
      </v-row>
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
        cols="3"
        class="shrink"
        :class="state.gals_total < 5 ? 'd-block' : 'd-none'"
      >
        <div
        >
          Select {{ 5 - state.gals_total }} more <span :class="state.gals_total < 4 ? 'd-inline' : 'd-none'">galaxies</span><span :class="state.gals_total == 4 ? 'd-inline' : 'd-none'">galaxy</span> before moving on.
        </div>
      </v-col>
      <v-col
        class="shrink"
        :class="state.gals_total >= 5 ? 'd-block' : 'd-none'"
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
