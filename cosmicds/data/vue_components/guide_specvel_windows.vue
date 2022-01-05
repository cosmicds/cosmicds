<template>
  <v-btn
    block
    color="amber accent-2"
    light
    elevation="2"
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
              Galaxies emit light.
            </v-card-text>
          </v-window-item>


          <v-window-item :value="2">
            <v-card-text>
              Pass light through a spectrometer which will separate the light into its different colors (like a prism) and tell you how much light there is at each color (or wavelength).
            </v-card-text>
          </v-window-item>

          <v-window-item :value="3">
            <v-card-text>
              <div>
                Certain atoms and molecules absorb or emit light at very specific known wavelengths, creating bright spikes (emission lines) or faint dips (absorption lines) in the spectrum.
              </div>
              <div>
                (Show images of sample spectra)
              </div>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="4">
            <v-card-text>
              <div>
                In your galaxy data, you will be looking for a specific hydrogen emission line (known as H-alpha) that emits at 6563 Angstroms at rest;  or a magnesium absorption line (known as Mg-II) that absorbs at ____ .
              </div>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="5">
            <v-card-text>
              <div>
                Firetruck siren - pitch gets higher when the truck is moving toward you; lower when truck is moving away.
              </div>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="6">
            <v-card-text>
              <div>
                In the same way, wavelength of light gets shorter (bluer) when it’s moving toward you; longer (redder) when it’s moving away from you.
              </div>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="7">
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
            :disabled="step === 7"
            color="primary"
            text
            @click="step++;"
          >
            {{ step < 7 ? 'next' : '' }}
          </v-btn>
          <v-btn
            :disabled="step < 7"
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
        case 1: return 'Light'
        case 2: return 'Spectrometer'
        case 3: return 'Atom & Molecule Emissions'
        case 4: return 'Lines to Look For'
        case 5: return 'Doppler, pt. I'
        case 6: return 'Doppler, pt. II'
        default: return 'Complete'
      }
    },
  },
};
</script>