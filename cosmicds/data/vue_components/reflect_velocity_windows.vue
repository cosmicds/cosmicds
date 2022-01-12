<template>
  <v-btn
  block
      color="info"
      dark
      @click.stop="dialog = true"
  >
    <v-icon
      class="mr-4"
    >
      mdi-pen
    </v-icon>
    {{ buttonText }}

    <v-dialog
        v-model="dialog"
        persistent
        max-width="800px"
    >
      <v-card
        class="mx-auto"
        max-width="800"
      >
        <v-card-title
          class="text-h6 font-weight-regular justify-space-between"
        >
          <span>{{ currentTitle }}</span>
          <v-avatar
            color="pink lighten-3"
            class="subheading white--text"
            size="24"
            v-text="step"
          ></v-avatar>
        </v-card-title>

        <v-window
          v-model="step"
          vertical
        >
          <v-window-item :value="1">
            <v-card-text>
              How do the observed wavelengths of emission or absorption lines in your galaxies
              compare with the “rest” wavelength of those lines?
              <mc-radiogroup
                radio-one="Lines in the galaxies have the same wavelength as the lines at rest."
                radio-two="Some galaxies have lines with smaller wavelengths and some have lines with larger wavelengths than the lines at rest."
                radio-three="Most or all of the galaxies have lines with smaller wavelengths than the lines at rest."
                radio-four="Most or all of the galaxies have lines with larger wavelengths than the lines at rest."
              >
              </mc-radiogroup>
            </v-card-text>
          </v-window-item>


          <v-window-item :value="2">
            <v-card-text>
              From the data you just collected, what can you conclude about how the galaxies are moving relative to our home galaxy, the Milky Way?
              <mc-radiogroup
                radio-one="The galaxies are not moving."
                radio-two="Some galaxies are moving toward our galaxy and some galaxies are moving away from our galaxy."
                radio-three="Galaxies are mostly moving toward our galaxy."
                radio-four="Galaxies are mostly moving away from our galaxy."
              >
              </mc-radiogroup>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="3">
            <v-card-text>
              Now that we agree the galaxies are not static, let’s calculate how fast these galaxies are moving.
              <v-row>
                <v-col cols = 6>
                </v-col>
                <v-col cols = 6>
                  <v-row>
                    <v-col cols = "5">
                      <v-text-field
                        label="observed wavelength"
                        outlined
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols = "2"
                      class="text-center"
                    >
                      -
                    </v-col>
                    <v-col cols = "5">
                      <v-text-field
                        label="rest wavelength"
                        outlined
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                      <v-divider class="mb-2"></v-divider>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols = "12">
                      <v-text-field
                        label="rest wavelength"
                        outlined
                      ></v-text-field>
                    </v-col>
                  </v-row>

                  <v-row>
                    <v-col cols = "12">
                      <v-text-field
                        label="observed - rest"
                        outlined
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                      <v-divider class="mb-2"></v-divider>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols = "12">
                      <v-text-field
                        label="rest wavelength"
                        outlined
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-col>
              </v-row>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="4">
            <div class="pa-4 text-center">
              <v-img
                class="mb-4"
                contain
                height="128"
                src="https://www.pngrepo.com/png/211744/512/rocket-ship-launch-missile.png"
              ></v-img>
              <h3 class="text-h6 font-weight-light mb-2">
                Nice work reflecting!
              </h3>
              <span class="text-caption grey--text">You can start plotting your data now.</span>
            </div>
          </v-window-item>
        </v-window>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn
            :disabled="step === 1"
            color="primary"
            text
            @click="step--"
          >
            Back
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            :disabled="step === 4"
            color="primary"
            text
            @click="step++;"
          >
            {{ step < 4 ? 'next' : '' }}
          </v-btn>
          <v-btn
            :disabled="step < 4"
            color="primary darken-1"
            depressed
            @click="() => { $emit('close'); dialog = false; }"
          >
            {{ closeText }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-btn>
</template>



<script>
module.exports = {
  props: ["buttonText", "titleText", "closeText"],
  data: function () {
    return {
      step: 1,
      dialog: false
    };
  },
  computed: {
    currentTitle () {
      switch (this.step) {
        case 1: return 'Observed vs. Rest Wavelengths'
        case 2: return 'How Galaxies Move'
        case 3: return 'Calculate Galaxy Velocity'
        default: return 'Complete'
      }
    },
  },
};
</script>