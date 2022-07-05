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
        Click the <v-icon>mdi-ruler</v-icon> icon to activate the angular size measuring tool.
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
            state.marker = 'ang_siz2'
          "
        >
          back
        </v-btn>
      <v-spacer></v-spacer>
      <v-col
        cols="6"
        class="shrink"
        v-if="!state.ruler_clicked"
      >
        <div
          style="font-size: 16px;"
        >
          Click the <v-icon>mdi-ruler</v-icon> icon.
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="state.ruler_clicked"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'ang_siz4'
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
