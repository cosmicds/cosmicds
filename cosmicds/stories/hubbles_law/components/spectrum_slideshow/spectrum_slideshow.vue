<template>
  <v-btn
    block
    color="secondary"
    elevation="2"
    @click.stop="dialog = true"
  >
    Learn More

    <v-dialog
        v-model="dialog"
        persistent
        max-width="1000px"
    >
      <v-card
        class="mx-auto"
      >
        <v-toolbar
          color="secondary"
          dense
          dark
        >
          <v-toolbar-title
            class="text-h6 text-uppercase font-weight-regular"
          >
            Light and Spectra
          </v-toolbar-title>
          <v-spacer></v-spacer>
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
        </v-toolbar>

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
                      Refraction and Diffraction
                    </h3>
                    <div>
                    <v-card
                      class="mt-auto white--text"
                      flat
                      color="secondary"
                    >                  
                      <v-card-text>
                        A <strong>spectrum</strong> is created when you pass light from a source through a <strong>spectrograph</strong>, which separates the light into its different colors (like a rainbow) and measures how much light there is at each color (or wavelength).
                      </v-card-text>
                    </v-card>
                    <br>               
                      <p>
                        The figure illustrates light passing through a diffraction grating (1) and a prism (2).
                      </p>
                      <p>
                        Diffraction gratings and prisms &#8212; and raindrops, bubbles, and oil slicks &#8212; create spectra because they bend light of different colors by different amounts. See link for more details.
                      </p>
                    </div>
                  </v-col>
                  <v-col cols="1">
                  </v-col>
                  <v-col cols="4">
                    <v-img
                      class="mb-4 mx-a"
                      contain                      
                      :src="`${state.image_location}/refraction_diffraction_spectra.png`"></v-img>
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
                      Spectrum images and graphs
                    </h3>
                    <div>                    
                      <v-card
                        class="mt-auto white--text"
                        flat
                        color="secondary"
                      > 
                        <v-card-text>
                          A <strong>spectrum</strong> is created when you pass light from a source through a <strong>spectrograph</strong>, which separates the light into its different colors (like a rainbow) and measures how much light there is at each color (or wavelength).
                        </v-card-text>
                      </v-card>
                      <br>
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

                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Light spectrum for LED bulb
                    </h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${state.image_location}/LED_White_spectool.png`"
                    ></v-img>
                    <h4>
                      Light spectrum for sodium vapor bulb
                    </h4>
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${state.image_location}/Sodium_Vapor_spectool.png`"
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
                      <v-card
                        class="mt-auto white--text"
                        flat
                        color="secondary"
                      > 
                        <v-card-text>
                          A <strong>spectrum</strong> is created when you pass light from a source through a <strong>spectrograph</strong>, which separates the light into its different colors (like a rainbow) and measures how much light there is at each color (or wavelength).
                        </v-card-text>
                      </v-card>
                      <br>
                      <p>
                        At wavelengths where the spectrum graph has a <strong>high brightness</strong> value, the spectrum image is <strong>brightly lit</strong> at the corresponding wavelengths.
                      </p>
                    </div>

                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Light spectrum for LED bulb
                    </h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${state.image_location}/LED_White_w_highlight_spectool.png`"
                    ></v-img>
                    <h4>
                      Light spectrum for sodium vapor bulb
                    </h4>
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${state.image_location}/Sodium_Vapor_w_highlight_spectool.png`"
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
                      Interpreting spectrum graphs
                    </h3>
                    <div>
                      <v-card
                        class="mt-auto white--text"
                        flat
                        color="secondary"
                      > 
                        <v-card-text>
                          A <strong>spectrum</strong> is created when you pass light from a source through a <strong>spectrograph</strong>, which separates the light into its different colors (like a rainbow) and measures how much light there is at each color (or wavelength).
                        </v-card-text>
                      </v-card>
                      <br>
                      <p>
                        At wavelengths where the spectrum graph has a <strong>low brightness</strong> value, the spectrum image is <strong>dim</strong> or <strong>dark</strong> at the corresponding wavelengths.
                      </p>
                    </div>

                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Light spectrum for LED bulb
                    </h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${state.image_location}/LED_White_w_neghighlight_spectool.png`"
                    ></v-img>
                    <h4>
                      Light spectrum for sodium vapor bulb
                    </h4>
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${state.image_location}/Sodium_Vapor_w_neghighlight_spectool.png`"
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
              <v-container>
                <v-row>
                  <v-col
                    cols="6"
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
                        This is due to a phenomenon called the <strong>Doppler shift</strong>, where the observed properties of a sound wave change due to the motion of the object emitting the sound.
                      </p>
                    </div>
                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Doppler Shift
                    </h4>
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${state.image_location}/siren_moving_white.png`"
                    ></v-img>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="5" 
            class="no-transition"
          >
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col
                    cols="6"
                  >
                    <h3
                      class="mb-4"
                    >
                      How do spectra tell us about a source's motion?
                    </h3>
                    <div>
                      <p>
                        The same <strong>Doppler shift</strong> happens with <strong>light</strong> (and all other wave phenomena), but a light source has to be moving very fast for you to notice these changes!
                      </p>
                      <p>
                        When a light source moves <strong>away from you</strong>, you observe the light to have a <strong>longer (redder)</strong> wavelength than you would if the object were not moving. This effect is called <strong>redshift</strong>.
                      </p>
                      <p>
                        When a light source moves <strong>toward you</strong>, you observe the light to have a <strong>shorter (bluer)</strong> wavelength than you would if the object were not moving. This effect is called <strong>blueshift</strong>.
                      </p>
                    </div>
                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Doppler Shift
                    </h4>
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${state.image_location}/doppler_shift_light_white.png`"
                    ></v-img>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="6" 
            class="no-transition"
          >
            <v-card-text>
              <v-container>
                <v-row no-gutters>
                  <v-col>
                    <h3
                      class="mb-4"
                    >
                      How do we know the wavelength of the light when the source is at rest?
                    </h3>
                    <div>
                      <p>
                        A key to using the Doppler Shift to determine the velocity of an astronomical source is to know the wavelength of its light when it is <strong>not</strong> moving. (This is called the <strong>rest wavelength</strong> of light).
                      </p>
                      <p>
                        Luckily, elements emit and absorb light at specific wavelengths that are unique to those elements, providing “chemical fingerprints” that we can use to identify the presence of an element in an astronomical source (like a star or a gas cloud). 
                      </p>
                      <p>
                        This image shows the pattern of emission lines that are produced by four different elements. The emission line patterns are unique to each element.
                      </p>
                    </div>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col
                    cols="2"
                    class="d-flex flex-column"
                    height="100%"
                  >
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${state.image_location}/carbon_atom_model.png`"
                    ></v-img>
                    <v-img
                      class="mt-auto mx-a"
                      contain
                      :src="`${state.image_location}/nitrogen_atom_model.png`"
                    ></v-img>
                  </v-col>
                  <v-col
                    cols="8"
                  >
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${state.image_location}/stsci_spectrum_element_montage.jpg`"
                    ></v-img>
                  </v-col>
                  <v-col
                    cols="2"
                    class="d-flex flex-column"
                    height="100%"
                  >
                    <v-row>
                      <v-col>
                        <v-img
                          class="mx-a"
                          contain
                          :src="`${state.image_location}/oxygen_atom_model.png`"
                        ></v-img>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-img
                          class="mt-auto mx-a"
                          contain
                          :src="`${state.image_location}/iron_atom_model.png`"
                        ></v-img>
                      </v-col>
                    </v-row>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>


          <v-window-item :value="7" 
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
                      Emission and absorption lines in spectra
                    </h3>
                    <div>
                      <p>
                        The top spectrum shows <strong>emission lines</strong> from a source containing hydrogen.
                      </p>
                      <p>
                        The bottom spectrum shows <strong>absorption lines</strong> due to hydrogen.
                      </p>
                      <p>
                        Notice that in both spectra, the emission and absorption lines are present at the same combination of wavelengths (hydrogen’s “chemical fingerprint”).
                      </p>
                    </div>
                    <v-card
                      class="mt-auto white--text"
                      flat
                      color="secondary"
                    > 
                      <v-card-text>
                        Elements emit light at specific wavelengths, and they can also absorb light at the same wavelengths, depending on the conditions associated with a light source.
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Hydrogen emission spectrum
                    </h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${state.image_location}/hydrogen_emission_spectool.png`"
                    ></v-img>
                    <h4>
                      Hydrogen absorption spectrum
                    </h4>
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${state.image_location}/hydrogen_absorption_spectool.png`"
                    ></v-img>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="8" 
            class="no-transition"
          >
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col
                    cols="12"
                  >
                    <p>
                      Since we know the wavelengths emitted or absorbed by an element when it is not moving, we can use these <strong>rest wavelengths</strong> as a reference to compare against the <strong>observed wavelengths</strong> of the light when an object is moving.
                    </p>
                </v-row>
                <v-row>
                  <v-col
                    cols="12"
                    lg="10"
                    offset-lg="1"
                  >
                    <p>
                      The dotted line shows the rest wavelength of a hydrogen line known as <strong>H-&alpha;</strong> (pronounced "H alpha"). The solid line shows the observed wavelength of the H-&alpha; line.
                    </p>
                    <v-img
                      contain
                      :src="`${state.image_location}/restobs1_spectool.png`"
                    >
                    </v-img>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="9" 
            class="no-transition"
          >
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col
                    cols="12"
                  >
                    <p>
                      Since we know the wavelengths emitted or absorbed by an element when it is not moving, we can use these <strong>rest wavelengths</strong> as a reference to compare against the <strong>observed wavelengths</strong> of the light when an object is moving.
                    </p>
                </v-row>
                <v-row>
                  <v-col
                    cols="12"
                    lg="10"
                    offset-lg="1"
                  >
                    <p>
                      The dotted line shows the rest wavelength of a hydrogen line known as <strong>Mg I</strong> (pronounced "magnesium one"). The solid line shows the observed wavelength of the Mg I line.
                    </p>
                    <v-img
                      contain
                      :src="`${state.image_location}/restobs2_spectool.png`"
                    >
                    </v-img>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="10" 
            class="no-transition"
          >
            <div class="pa-4 text-center my-auto">
              <v-img
                class="mb-4"
                contain
                height="128"
                src="https://www.pngrepo.com/png/211744/512/rocket-ship-launch-missile.png"
              ></v-img>
              <h3 class="text-h6 font-weight-light mb-2">
                You're ready to start measuring galaxy velocities now.
              </h3>
              <span class="text-caption grey--text">Click on "LEARN MORE" if you'd like to come back for a refresher.</span>
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
            :disabled="step === 10"
            color="accent"
            text
            @click="step++;"
          >
            {{ step < 10 ? 'next' : '' }}
          </v-btn>
          <v-btn
            :disabled="step < 10"
            color="accent"
            class="black--text"
            depressed
            @click="() => { $emit('close'); dialog = false; step = 0; }"
          >
            Done
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-btn>
</template>


<style>

.no-transition {
  transition: none !important;
}

</style>
