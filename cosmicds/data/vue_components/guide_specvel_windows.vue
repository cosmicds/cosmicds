<template>
  <v-btn
    block
    color="primary"
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
          <span>
            <v-avatar
              color="info"
              class="subheading white--text mr-4"
              size="24"
              v-text="step"
            ></v-avatar>
            {{ currentTitle }}
          </span>
          <span
            @click="() => { $emit('close'); dialog = false; if (step == 6)  {step = 0}; }"
          >
            <v-btn
              icon
            >
              <v-icon>
                mdi-close
              </v-icon>
            </v-btn>
          </span>
        </v-card-title>

        <v-window
          style="min-height: 250px;"
          v-model="step"
        >
          <v-window-item :value="0" 
            class="no-transition"
          >
            <v-card-text>
              Galaxies emit light.
            </v-card-text>
          </v-window-item>


          <v-window-item :value="1" 
            class="no-transition"
          >
            <v-card-text>
              Pass light through a spectrometer which will separate the light into its different colors (like a prism) and tell you how much light there is at each color (or wavelength).
            </v-card-text>
          </v-window-item>

          <v-window-item :value="2" 
            class="no-transition"
          >
            <v-card-text>
              <div>
                Certain atoms and molecules absorb or emit light at very specific known wavelengths, creating bright spikes (emission lines) or faint dips (absorption lines) in the spectrum.
              </div>
              <div>
                (Show images of sample spectra)
              </div>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="3" 
            class="no-transition"
          >
            <v-card-text>
              <div>
                In your galaxy data, you will be looking for a specific hydrogen emission line (known as H-alpha) that emits at 6563 Angstroms at rest;  or a magnesium absorption line (known as Mg-II) that absorbs at ____ .
              </div>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="4" 
            class="no-transition"
          >
            <v-card-text>
              <div>
                Firetruck siren - pitch gets higher when the truck is moving toward you; lower when truck is moving away.
              </div>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="5" 
            class="no-transition"
          >
            <v-card-text>
              <div>
                In the same way, wavelength of light gets shorter (bluer) when it’s moving toward you; longer (redder) when it’s moving away from you.
              </div>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="6" 
            class="no-transition"
          >
            <div class="pa-4 text-center">
              <v-img
                class="mb-4"
                contain
                height="128"
                src="https://www.pngrepo.com/png/211744/512/rocket-ship-launch-missile.png"
              ></v-img>
              <h3 class="text-h6 font-weight-light mb-2">
                You're ready to start measuring galaxy velocities now.
              </h3>
              <span class="text-caption grey--text">Click on "Info" if you'd like to come back for a refresher.</span>
            </div>
          </v-window-item>
        </v-window>

        <v-divider></v-divider>

        <v-card-actions
          class="justify-space-between"
        >
          <v-btn
            :disabled="step === 0"
            color="accent"
            text
            @click="step--"
          >
            Back
          </v-btn>
          <v-spacer></v-spacer>
          <v-item-group
            v-model="step"
            class="text-center"
            mandatory
          >
            <v-item
              v-for="n in length"
              :key="`btn-${n}`"
              v-slot="{ active, toggle }"
            >
              <v-btn
                :input-value="active"
                icon
                @click="toggle"
              >
                <v-icon>mdi-record</v-icon>
              </v-btn>
            </v-item>
          </v-item-group>
          <v-spacer></v-spacer>
          <v-btn
            :disabled="step === 6"
            color="accent"
            text
            @click="step++;"
          >
            {{ step < 6 ? 'next' : '' }}
          </v-btn>
          <v-btn
            :disabled="step < 6"
            color="accent"
            class="black--text"
            depressed
            @click="() => { $emit('close'); dialog = false; step = 0; }"
          >
            {{ closeText }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-btn>
</template>


<style>

.no-transition {
  transition: none;
}

</style>


<script>
module.exports = {
  props: ["buttonText", "titleText", "closeText"],
  data: function () {
    return {
      step: 0,
      length: 7,
      dialog: false
    };
  },
  computed: {
    currentTitle () {
      switch (this.step) {
        case 0: return 'Light'
        case 1: return 'Spectrometer'
        case 2: return 'Atom & Molecule Emissions'
        case 3: return 'Lines to Look For'
        case 4: return 'Doppler, pt. I'
        case 5: return 'Doppler, pt. II'
        default: return 'Complete'
      }
    },
  },
};
</script>

<style>

div {
  color: "purple";
}

</style>