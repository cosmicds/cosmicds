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
      Rest Wavelength
    </h3>
    <div
      class="mb-4"
    >
      <p
        v-if="!state.lambda_on"      
      >
        Your galaxy spectrum has {{ state.element == 'Mg-I' ? 'a' : 'an' }} {{ state.element }} {{ state.element == 'Mg-I' ? 'absorption' : 'emission' }} line marked.
      </p>
      <p
        v-if="!state.lambda_used"
      >
        The known <strong>rest wavelength</strong> for the line is recorded in your table.
      </p>
      <p
        v-if="!state.lambda_on"
      >
        Click the <v-icon>mdi-lambda</v-icon> icon in the Spectrum Viewer toolbar to display the line's rest wavelength on the graph.
      </p>
      <p
        v-if="state.lambda_on"
      >
        The rest wavelength of your line appears in the graph as a vertical dotted line.
      </p>
      <p
        v-if="state.lambda_on"
      >
        You can click the <v-icon>mdi-lambda</v-icon> icon again to toggle the rest wavelength back off.
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
            state.marker = 'mee_spe1';
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      
      <v-col
        cols="6"
        class="shrink"
        v-if="!state.lambda_used"
      >
        <div
          style="font-size: 16px;"
        >
          Click the <v-icon>mdi-lambda</v-icon> button.
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="state.lambda_used"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'obs_wav1';
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
