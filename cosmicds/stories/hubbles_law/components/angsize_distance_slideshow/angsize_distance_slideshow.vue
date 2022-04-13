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
            @click="() => { $emit('close'); dialog = false; if (step == 8)  {step = 0}; }"
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
                <v-row> 
                  <v-col>
                    <h3 class="mb-4"> 1920's Astronomy </h3>
                    <div>
                      <p>
                        You’ve now uncovered evidence that galaxies are for the most part moving AWAY from our Milky Way galaxy. To scientists in the 1920’s, this led to a radical shift in their world view. Once they knew galaxies do not, in fact, move about randomly, they needed to come up with a new explanation for this surprising phenomenon.
                      </p>
                    </div>
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
                <v-row>
                  <v-col>
                  <h3 class="mb-4"> 1920's Astronomy </h3>
                    <div>                    
                     <p>
                        Edwin Hubble was an astronomer who was interested in these galaxies. After looking at Slipher’s velocity measurements, Hubble wondered if there is a relationship between the galaxies’ velocities and their distances from the Milky Way. 
                     </p>
                     <p>
                        Measuring distances to objects in space is one of the most challenging things to do in astronomy. In the next section, you will learn a method for determining distances to galaxies.
                      </p>
                    </div>
                    </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="2" class="no-transition">
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col
                    cols="6"
                    class="d-flex flex-column"
                    height="100%"
                    flat
                    tile
                  >
                    <h3 class="mb-4">Refraction and Diffraction</h3>
                    <div>
                      <p>
                         Consider the people in this image. Do you think that there really is a giant sized person about to step on a smaller person?
                        </p>
                      <br>
                      <p>
                        No! The people are not at the same distance from the photographer. 
                      </p>
                    </div>
                  </v-col>
                  <v-col cols="6">
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${state.image_location}/People near and far labeled.png`"
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
                <v-row>
                  <v-col>
                    <h3 class="mb-4">
                      Distance and Apparent Size
                    </h3>
                  <div>
                    <p>  
                      From looking at these images, can you determine which person and which galaxy are closest to the viewer? What visual clues and assumptions do you need to make this estimation?
                    </p>
                  </div>
                    <v-row>
                        <v-col cols="6" > 
                          <h4>
                            People on the beach 
                          </h4>
                          <v-img
                            class="mb-4 mx-a"
                            contain
                            :src="`${state.image_location}/People near and far labeled.png`"
                          ></v-img>
                          </v-col>
                        <v-col cols="6">
                          <h4>
                            Galaxies in the night sky 
                          </h4>
                          <v-img
                            class="mb-4 mx-a"
                            contain
                            :src="`${state.image_location}/galaxies A B boxed - Harry may update with nicer boxes.png`"
                          ></v-img>
                        </v-col>
                      </v-row>
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
                  <v-col>
                    <h3
                      class="mb-4"
                    >
                      Distance and Apparent Size
                    </h3>
                    <div>
                    <p>
                      You know how big a typical person is, and people are generally similar in size to each other, so the ones that are closest to you will appear bigger than the ones that are farthest away.
                    </p>
                    <p>
                      If we make the same assumption about galaxies, you can use this information to determine how far away they are.
                    </p>
                    <v-row>
                      <v-col cols="6">
                        <h4>
                          People on the beach 
                        </h4>
                        <v-img
                          class="mb-4 mx-a"
                          contain
                          :src="`${state.image_location}/People near and far labeled.png`"
                        ></v-img>
                      </v-col>
                      <v-col cols="6">
                      <h4>
                        Galaxies in the night sky 
                      </h4>
                      <v-img
                        class="mb-4 mx-a"
                        contain
                        :src="`${state.image_location}/galaxies A B boxed - Harry may update with nicer boxes.png`"
                      ></v-img>
                      </v-col> 
                      </v-row> 
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
                      :src="`${state.image_location}/Erin's Pinky - to be replaced with Anna figure.png`"
                    ></v-img>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="6" 
          >
            <v-card-text >
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
                        color="info"
                        v-intersect = "(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
                      >
                      <v-card-text>
                      <p>
                        $$ \text{Galaxy's Angular Size} (\theta) = $$ $$ \frac{\text{Galaxy's Physical Length} (L)}{\text{Galaxy's Distance} (D)} $$  
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
                      :src="`${state.image_location}/esahubble_potw2031a_1600_cleaned.jpg`"
                    ></v-img>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="7" 
            class="no-transition"
          >
          <v-card-text >
              <v-container>
                <v-row>
                    <v-col cols="7"> 
                      <div>
                      <v-row>
                        <h3 class="mb-4">
                          Reflect
                        </h3>  
                           
                        <p>
                          Let’s come back to these galaxies. Use the image to estimate how much farther away Galaxy B is than Galaxy A. Assume galaxies A and B have the same physical size.
                        </p>
                        <v-card
                          class="mt-auto white--text"
                          flat
                          color="info"
                        >
                          <v-card-text v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}">
                            <p>
                              $$ \text{Galaxy's Angular Size} (\theta) = $$ $$ \frac{\text{Galaxy's Physical Length} (L)}{\text{Galaxy's Distance} (D)} $$ 
                            </p>
                          </v-card-text>
                        </v-card>
                      </v-row>
                      <v-row>
                    <mc-radiogroup
                      :radio-options="[
                        'Galaxy A and Galaxy B are the same distance away from us.',
                        'Galaxy A is farther away from us than Galaxy B.',
                        'Galaxy A is closer to us than Galaxy B.',
                        'We do not have enough information to answer this question']"
                      :feedbacks="['Try again.', 'That\'s right!', 'Try again.', 'Try again.']"
                      :answer-key="1"
                    >
                      </mc-radiogroup>
                      </v-row>
                   </div>
                </v-col> 
                <v-col cols="5">
                  <h4>
                    Galaxy Picture
                  </h4>
                  <v-img
                    class="mx-a"
                    contain
                    :src="`${state.image_location}/galaxies A B boxed - Harry may update with nicer boxes.png`"
                  ></v-img>
                </v-col>
              </v-row> 
              <v-container>            
            </v-card-text>
          </v-window-item>


          <v-window-item :value="8" 
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
                      Distance and apparent size
                    </h3>
                    <div>
                      <p>
                       Nice work! We’re going to use this formula to measure distances to your galaxies. 
                      </p>
                       <v-card
                        class="mt-auto white--text"
                        flat
                        color="info"
                      >
                      <v-card-text v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}">
                      <p>
                        $$ \text{Galaxy's Angular Size} (\theta) = $$ $$ \frac{\text{Galaxy's Physical Length} (L)}{\text{Galaxy's Distance} (D)} $$ 
                      </p>
                      </v-card-text>
                      </v-card>
                      <p>
                        With some algebra and unit conversions, this becomes: 
                      </p>
                      <p>
                        Galaxy Distance = 200,000 x physical length of galaxy / Galaxy’s angular size (theta, in arcseconds)
                      </p>
                      <p>
                        In a few moments, we will teach you how to measure the angular size of your galaxies.
                      </p>
                      <p>
                        But first, we need to know the physical length of your galaxy. In this data story, we are going to make an assumption that all galaxies are the <strong>same physical length as the Milky Way galaxy</strong>, which we know to be about 100,000 light years across. 
                      </p>
                      <p>
                        You can ponder later whether you think this is a good or bad assumption.
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
                      :src="`${state.image_location}/esahubble_potw2031a_1600_cleaned.jpg`"
                    ></v-img>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="9" 
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
            id = "next_button"
            :disabled = "step === 8 || step === 7"
            color="accent"
            text
            @click="step++;"
          >
            {{ step < 8 ? 'next' : '' }}
          </v-btn>
          <v-btn
            :disabled = "step < 8"
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
