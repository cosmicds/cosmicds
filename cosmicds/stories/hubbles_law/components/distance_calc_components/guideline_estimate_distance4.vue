<template>
  <v-alert
    color="info"
    class="mb-4 mx-auto angsize_alert"
    max-width="800"
    elevation="6"
  >
    <h3
      class="mb-4"
    >
      Estimate Distance
    </h3> 

    <div
      class="mb-4"
      v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
    >
      <v-card
        class="JaxEquation past_block pa-3"
      >
        $$ D = \frac{ {{ Math.round(distance_const) }} }{\textcolor{black}{\colorbox{#FFAB91}{ {{ (state.meas_theta).toFixed(0) }} } }} $$
      </v-card>    
      <p>
        Dividing through gives you the estimated distance.
      </p>
      <div
        class="JaxEquation my-8"
      >
        $$ D = {{ (Math.round(distance_const)/state.meas_theta).toFixed(0) }} \text{ Mpc} $$
      </div>
      <v-divider role="presentation" class="mt-3"></v-divider>
      <v-card
        outlined
        class="legend mt-8"
        color="info"
      >
        <v-container>
          <v-row
            no-gutters
          >
            <v-col>
              <div
                class="JaxEquation"
              >
                $$ D = \frac{ {{ Math.round(distance_const) }} }{\theta} $$
              </div>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <v-row
            no-gutters
            class="my-1"
          >
            <v-col>
              \(D\)
            </v-col>
            <v-col
              cols="10"
            >
              distance to your galaxy, in Mpc
            </v-col>
          </v-row>
          <v-row
            no-gutters
            class="my-1"
          >
            <v-col
              cols="2"
            >
              \(&theta;\)
            </v-col>
            <v-col
              cols="10"
            >
              angular size of your galaxy, in arcseconds
            </v-col>
          </v-row>
        </v-container>
      </v-card>
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
            state.marker = 'est_dis3';
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      <v-col
        class="shrink"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click=" () => {
            state.marker = 'fil_rem1';
            state.distance_calc_count += 1;
          }"
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert> 
</template>

<style>

.JaxEquation .MathJax {
  margin: 16px auto !important;
}

mjx-mfrac {
  margin: 0 4px !important;
}

mjx-mstyle {
  border-radius: 5px;
}

.angsize_alert .v-alert {
  font-size: 16px !important;
}

.v-application .legend {
  border: 1px solid white !important;
  max-width: 300px;
  margin: 0 auto 0;
  font-size: 15px !important;
}

#gal_ang_size {
  color:  black;
  font-size: 18px;
  font-family: "Roboto", Arial, Helvetica, sans-serif;
  padding: 3px;
}


</style>

