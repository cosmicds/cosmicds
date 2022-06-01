<template>
  <v-alert
    class="mb-4"
    color="info"
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
      <p>
        Your galaxy spectrum has either an H-&alpha; emission line or a Mg-I absorption line marked.
      </p>
      <p>
        The known <strong>rest wavelength</strong> for the line is recorded in your table.
      </p>
      <p>
        Click the <v-icon>mdi-lambda</v-icon> icon in the viewer header to display the rest wavelength for that line. 
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
        v-if="!state.lambda_clicked"
      >
        <div
          style="font-size: 16px;"
        >
          Click <v-icon>mdi-lambda</v-icon> button.
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="state.lambda_clicked"
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
