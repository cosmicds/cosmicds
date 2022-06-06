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
      Meet the Spectrum Viewer
    </h3>
    <div
      class="mb-4"
    >
      <p>
        Here is a spectrum of light measured from your chosen galaxy.
      </p>
      <p>
        Click the LEARN MORE button to learn how a spectrum can reveal if an object (such as a galaxy) is moving toward or away from an observer.
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
        v-if="!state.vel_win_opened"
      >
        <div
          style="font-size: 16px;"
        >
          Click the LEARN MORE button.
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="state.vel_win_opened"
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
