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
        max-width="1000px"
    >
      <v-card
        class="mx-auto"
      >
        <v-card-title
          class="text-h6 font-weight-regular justify-space-between"
          dense
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
          v-model="step"
          style="height: 70vh;"
          class="overflow-auto"
        >
          <v-window-item :value="0" 
            class="no-transition"
          >
            <v-card-text>
              <v-container>
                <v-row
                >
                  <v-col
                    cols="6" 
                    class="d-flex flex-column"
                    height="100%"
                    flat
                    tile
                  >
                    <h3
                      class="mb-4"
                    >
                      Spectrum images and graphs
                    </h3>
                    <div>
                      <p>
                        These graphics show sample spectra for two different types of light bulbs.
                      </p>
                      <p>
                        The spectrum images (top) show what the light looks like when it is separated into its colors by the spectrograph. 
                      </p>
                      <p>
                        The spectrum graphs (bottom) represent how bright the light is at each specific wavelength.
                      </p>
                    </div>
                    <v-card
                      class="mt-auto white--text"
                      flat
                      color="secondary"
                    > 
                      <v-card-text>
                        A <strong>spectrum</strong> is created when you pass light from a source through a <strong>spectrograph</strong>, which separates the light into its different colors (like a rainbow) and measures how much light there is at each color (or wavelength).
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Light spectrum for LED bulb
                    </h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      src="../data/images/LED_White_spectool.png"
                    ></v-img>
                    <h4>
                      Light spectrum for sodium vapor bulb
                    </h4>
                    <v-img
                      class="mx-a"
                      contain
                      src="../data/images/Sodium_Vapor_spectool.png"
                    ></v-img>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>


          <v-window-item :value="1" 
            class="no-transition"
          >
            <v-card-text>
              <v-container>
                <v-row
                >
                  <v-col
                    cols="6" 
                    class="d-flex flex-column"
                    height="100%"
                    flat
                    tile
                  >
                    <h3
                      class="mb-4"
                    >
                      Interpreting spectrum graphs
                    </h3>
                    <div>
                      <p>
                        At wavelengths where the spectrum graph has a <strong>high brightness</strong> value, the spectrum image is <strong>brightly lit</strong> at the corresponding wavelengths.
                      </p>
                    </div>
                    <v-card
                      class="mt-auto white--text"
                      flat
                      color="secondary"
                    > 
                      <v-card-text>
                        A <strong>spectrum</strong> is created when you pass light from a source through a <strong>spectrograph</strong>, which separates the light into its different colors (like a rainbow) and measures how much light there is at each color (or wavelength).
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Light spectrum for LED bulb
                    </h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      src="../data/images/LED_White_w_highlight_spectool.png"
                    ></v-img>
                    <h4>
                      Light spectrum for sodium vapor bulb
                    </h4>
                    <v-img
                      class="mx-a"
                      contain
                      src="../data/images/Sodium_Vapor_w_highlight_spectool.png"
                    ></v-img>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="2" 
            class="no-transition"
          >
            <v-card-text>
              <v-container>
                <v-row
                >
                  <v-col
                    cols="6" 
                    class="d-flex flex-column"
                    height="100%"
                    flat
                    tile
                  >
                    <h3
                      class="mb-4"
                    >
                      Interpreting spectrum graphs
                    </h3>
                    <div>
                      <p>
                        At wavelengths where the spectrum graph has a <strong>low brightness</strong> value, the spectrum image is <strong>dim</strong> or <strong>dark</strong> at the corresponding wavelengths.
                      </p>
                    </div>
                    <v-card
                      class="mt-auto white--text"
                      flat
                      color="secondary"
                    > 
                      <v-card-text>
                        A <strong>spectrum</strong> is created when you pass light from a source through a <strong>spectrograph</strong>, which separates the light into its different colors (like a rainbow) and measures how much light there is at each color (or wavelength).
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Light spectrum for LED bulb
                    </h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      src="../data/images/LED_White_w_neghighlight_spectool.png"
                    ></v-img>
                    <h4>
                      Light spectrum for sodium vapor bulb
                    </h4>
                    <v-img
                      class="mx-a"
                      contain
                      src="../data/images/Sodium_Vapor_w_neghighlight_spectool.png"
                    ></v-img>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="3" 
            class="no-transition"
          >
           <v-card-text>
              <v-container>
                <v-row
                >
                  <v-col
                    cols="6" 
                    class="d-flex flex-column"
                    height="100%"
                    flat
                    tile
                  >
                    <h3
                      class="mb-4"
                    >
                      How do spectra tell us about a source's motion?
                    </h3>
                    <div>
                      <p>
                        You have probably heard the pitch of a fire truck siren change as the truck is moving toward or away from you. When the truck is moving toward you, the siren’s pitch is higher, and when the truck is moving away from you, the siren’s pitch is lower. The faster the truck is moving, the bigger the change in pitch.
                      </p>
                      <p>
                        This is due to a phenomenon called the <strong>Doppler Shift<strong>, where the observed properties of a sound wave change due to the motion of the object emitting the sound.
                      </p>
                    </div>
                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Doppler Effect
                    </h4>
                    <v-img
                      class="mx-a"
                      contain
                      src="../data/images/siren_moving.png"
                    ></v-img>
                  </v-col>
                </v-row>
              </v-container>
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
        case 0: return 'Light and Spectra'
        case 1: return 'Light and Spectra'
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