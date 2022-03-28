<template>
  <v-alert
    class="mb-4"
    color="info"
    elevation="6"
  >
    <h3
      class="mb-4"
    >
      Meet the Spectrum Tool
    </h3>
    <div
      class="mb-4"
    >
      <p>
        To the right is a spectrum of light from your chosen galaxy.
      </p>
      <p>
        Let’s learn how a spectrum can tell us if an object is moving toward or away from us.
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
            state.marker = 'cho_row1';
            state.spectrum_tool_visible = 0;
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      
      <v-col
        cols="6"
        class="shrink"
        v-if="!state.vel_win_unopened"
      >
        <div
        >
          Click INFO button.
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="!state.vel_win_unopened"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'res_wav1';
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
