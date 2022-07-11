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
      Angular Size Measurement
    </h3>
    <div
      class="mb-4"
    >
      <p>
        Notice your galaxy’s angular size is now displayed in the table.
      </p>
      <p>
        You may adjust your measurement by clicking on the ends of the green line and moving them to a new location.
      </p>
      <p>
        Click <strong>DO'S AND DONT'S</strong> for tips on how to ensure the most accurate results.
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
            state.marker = 'ang_siz4'
          "
        >
          back
        </v-btn>
      <v-spacer></v-spacer>
      <v-col
        cols="6"
        class="shrink"
        v-if="!state.dos_donts_opened"
      >
        <div
          style="font-size: 16px;"
        >
          Click the <strong>DO'S AND DONT'S</strong> button.
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="state.dos_donts_opened"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'ang_siz6'
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
