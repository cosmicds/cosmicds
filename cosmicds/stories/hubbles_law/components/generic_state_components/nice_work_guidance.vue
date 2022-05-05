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
      Nice Work
    </h3>

    <div
      class="mb-4"
    >
      <p>
        As scientists do, let’s examine what conclusions you might draw from your data.
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
            state.marker = 'rep_rem1'
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      <v-col
        v-if="!state.spec_reflect_complete"
        cols="4"
        class="shrink"
      >
        <div
          style="font-size: 16px;"
        >
          Complete the REFLECT sequence to move on
        </div>
      </v-col>
      <v-col
        v-if="state.spec_reflect_complete"
        class="shrink"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'dop_cal1'
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
