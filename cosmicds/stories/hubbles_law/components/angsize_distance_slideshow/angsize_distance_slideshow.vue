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
    Info

    <v-dialog
        v-model="dialog"
        persistent
        max-width="1000px"
    >
      <v-card
        class="mx-auto"
      >
        <v-card-title
          class="text-h6 font-weight-regular justify-space-between my-0"
        >
          <span>
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
                
                    <div>
                    <v-card
                      class="mt-auto white--text"
                      flat
                      color="secondary"
                    >                  
                      <v-card-text>
                        You’ve now uncovered evidence that galaxies are for the most part moving AWAY from our Milky Way galaxy. To scientists in the 1920’s, this led to a radical shift in their world view. Once they knew galaxies do not, in fact, move about randomly, they needed to come up with a new explanation for this surprising phenomenon.
                      </v-card-text>
                    </v-card>
                    <br>               
                      <p>
                        You’ve now uncovered evidence that galaxies are for the most part moving AWAY from our Milky Way galaxy. To scientists in the 1920’s, this led to a radical shift in their world view. Once they knew galaxies do not, in fact, move about randomly, they needed to come up with a new explanation for this surprising phenomenon.
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
                    <div>                    
                      <v-card
                        class="mt-auto white--text"
                        flat
                        color="secondary"
                      > 
                        <v-card-text>
                          <p>
                            Edwin Hubble was an astronomer who was interested in these galaxies. After looking at Slipher’s velocity measurements, Hubble wondered if there is a relationship between the galaxies’ velocities and their distances from the Milky Way. 
                          </p>
                          <p>
                            Measuring distances to objects in space is one of the most challenging things to do in astronomy. In the next section, you will learn a method for determining distances to galaxies.
                          </p>
                        </v-card-text>
                      </v-card>
                      <br>
                     <p>
                        Edwin Hubble was an astronomer who was interested in these galaxies. After looking at Slipher’s velocity measurements, Hubble wondered if there is a relationship between the galaxies’ velocities and their distances from the Milky Way. 
                     </p>
                     <p>
                        Measuring distances to objects in space is one of the most challenging things to do in astronomy. In the next section, you will learn a method for determining distances to galaxies.
                      </p>
                    </div>
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
                      Distance and Apparent Size
                    </h3>
                    <div>
                      <v-card
                        class="mt-auto white--text"
                        flat
                        color="secondary"
                      > 
                        <v-card-text>
                         From looking at these images, can you determine which car and which galaxy are closest to the viewer? What visual clues and assumptions do you need to make this estimation?
                        </v-card-text>
                      </v-card>
                      <br>
                      <p>
                        From looking at these images, can you determine which car and which galaxy are closest to the viewer? What visual clues and assumptions do you need to make this estimation?
                      </p>
                    </div>

                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Cars in a parking lot
                    </h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${state.image_location}/LED_White_w_highlight_spectool.png`"
                    ></v-img>
                    <h4>
                      Galaxies in the night sky 
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
                      Distance and Apparent Size
                    </h3>
                    <div>
                      <v-card
                        class="mt-auto white--text"
                        flat
                        color="secondary"
                      > 
                        <v-card-text>
                          <p>
                            Question Here?
                          </p>
                          <p>
                            You know roughly how big a car is, and all types of cars are similar in size to each other, so the ones that are closest to you will appear bigger than the ones that are farthest away.
                          </p>
                          <p>
                          If we make the same assumption about galaxies, you can use this information to determine how far away they are.
                          </p>
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
                      Car in parking lots 
                    </h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${state.image_location}/LED_White_w_neghighlight_spectool.png`"
                    ></v-img>
                    <h4>
                      Galaxies in the night sky 
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
                      How to measure apparent size
                    </h3>
                    <div>
                    <p>
                     We need a way to measure “how big” an object seems. We call this “apparent” or “angular” size.
                    </p>
                    <p>
                    The apparent (or <strong> angular </strong> ) size of objects in the sky is measured in degrees, or in fractions of a degree. 
                    </p>
                    <p>
                    To get a sense for how big 1 degree is, hold your pinky out at arm’s length. Your pinky fingernail at arm’s length covers about 1 degree of arc in the sky.
                    </p>
                    <v-card
                        class="mt-auto white--text"
                        flat
                        color="secondary"
                      > 
                        <v-card-text>
                          <p>
                            <strong> Bonus experiment </strong> : Do you think your pinky held at arm’s length would cover the moon? 
                            Try it the next time you see the moon in the sky!

                          </p>
                        </v-card-text>
                        </v-card>
                    </div>
                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Anna Pointing Picture 
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
            <v-card-text v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}">
              $$ a = b + \frac{c}{d} $$
              <v-container>
                <v-row>
                  <v-col
                    cols="6"
                  >
                    <h3
                      class="mb-4"
                    >
                      Distance and apparent size
                    </h3>
                    <div>
                      <p>
                        As with the cars, if we know the physical length of a galaxy, then its angular size tells us its distance from us. 
                      </p>
                      <p>
                        For very far away objects like galaxies, the relationship is described by the formula:
                      </p>
                       <v-card
                        class="mt-auto white--text"
                        flat
                        color="secondary"
                      >
                      <v-card-text>
                      <p>
                        $$ \text{Galaxy's Angular Size} (\theta) = \frac{\text{Galaxy's Physical Length} (L)}{\text{Galaxy's Distance} (D)}}$$
                      </p>
                      <h6>
                        (ask your instructor for more information if you want to know how to use trigonometry to derive this formula).
                      </h6> 
                      </v-card-text>
                      </v-card>
                      <p>
                        For galaxies that are the same size, the larger the distance, the smaller galaxy will appear in angular size.   
                      </p>
                    </div>
                  </v-col>
                  <v-col cols="6">
                    <h4>
                      Galaxy Picture
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
=
          <v-window-item :value="6" 
            class="no-transition"
          >
          <h3 class="mb-4">
            Reflect
          </h3>

            <v-card-text>
               <p>
                  $ \text{Galaxy's Angular Size} (\theta) = \frac{\text{Galaxy's Physical Length} (L)}{\text{Galaxy's Distance} (D)}}$
                </p>
                <h5>
                  (ask your instructor for more information if you want to know how to use trigonometry to derive this formula).
                </h5> 
              <mc-radiogroup
                :radio-options="[
                  'Galaxy A and Galaxy B are the same distance away from us.',
                  'Galaxy A is farther away from us than Galaxy B.',
                  'Galaxy A is closer to us than Galaxy B.',
                  'We do not have enough information to answer this question']"
                  :feedbacks="['Try again.', 'That\'s right!', 'Try again.', 'Try again.']"
                :answer-key="3"
              >
              </mc-radiogroup>
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
            Done
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
