<template>
  <v-card
    elevation="6"
  >
    <v-toolbar
      color="info"
      dense
      dark
    >
      <v-toolbar-title
        class="text-h6 text-uppercase font-weight-regular"
      >
        {{ currentTitle }}
      </v-toolbar-title>
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
            <v-row> 
              <v-col>
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


      <v-window-item :value="2"
        class="no-transition"
      >
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
                <h3
                  class="mb-4"
                >
                  Distance and Apparent Size
                </h3>
                <div>
                  <p>
                    Consider the people in this image. Do you think that there really is a giant sized person holding a smaller person in their hand?
                  </p>
                  <p>
                    No! The people are not at the same distance from the photographer. 
                  </p>
                </div>
              </v-col>
              <v-col
                cols="6"
              >
                <h4
                  class="mb-2"
                >
                  Large and Small People?
                </h4>
                <v-img
                  class="mb-4 mx-a"
                  contain
                  :src="`${state.image_location}/People near and far - will replace with uncopyrighted.png`"
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
                <h3
                  class="mb-4"
                >
                  Distance and Apparent Size
                </h3>
                <div>
                  <p>  
                  From looking at these images, can you determine which person and which galaxy are closer to the viewer? What visual clues and assumptions do you need to make this estimation?
                  </p>
                </div>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="6"
              >
                <h4
                  class="mb-2"
                >
                  People on the beach 
                </h4>
                <v-img
                  class="mb-4 mx-a"
                  contain
                  :src="`${state.image_location}/People near and far - will replace with uncopyrighted.png`"
                ></v-img>
              </v-col>
              <v-col
                cols="6"
              >
                <h4
                  class="mb-2"
                >
                  Galaxies in the night sky 
                </h4>
                <v-img
                  class="mb-4 mx-a"
                  contain
                  :src="`${state.image_location}/esahubble_potw2031a_1600_cleaned.jpg`"
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
                    If we make the same assumption about galaxies, you can use this information to <b>determine how far away</b> they are.
                  </p>
                </div>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="6"
              >
                <h4
                  class="mb-2"
                >
                  People on the beach 
                </h4>
                <v-img
                  class="mb-4 mx-a"
                  contain
                  :src="`${state.image_location}/People near and far labeled.png`"
                ></v-img>
              </v-col>
              <v-col cols="6">
                <h4 class="mb-2">
                  Galaxies in the night sky 
                </h4>
                <v-img
                  class="mb-4 mx-a"
                  contain
                  :src="`${state.image_location}/esahubble_potw2031a_1600_cleaned.jpg`"
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
              <v-col>
                <h3>
                  How to measure apparent size
                </h3>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="8"
              >
                <p>
                  We need a way to measure “how big” an object seems. We call this “apparent” or “angular” size.
                </p>
                <p>
                  The apparent (or <strong>angular</strong>) size of objects in the sky is measured in degrees, or in fractions of a degree. 
                </p>
                <p>
                  To get a sense for how big 1 degree is, hold your pinky out at arm’s length. Your pinky fingernail at arm’s length covers about 1 degree of arc in the sky.
                </p>
              </v-col>
              <v-col
                cols="4"
              >
                <v-card
                  class="mt-auto white--text"
                  flat
                  color="secondary"
                > 
                  <v-card-text>
                    <p>
                      <strong>Bonus experiment</strong>: Do you think your pinky held at arm’s length would cover the moon? 
                      Try it the next time you see the moon in the sky!
                    </p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-row 
              justify="center"
            >
              <h4
                class="mb-2"
              >
                One degree of angular size in the sky is a pinky's width at arm's length. 
              </h4>
              <v-img
                class="mx-a"
                contain
                max-height="300"
                :src="`${state.image_location}/ErinPinkyAnnaArt.png`"
              ></v-img>
            </v-row>
          </v-container>
        </v-card-text>
      </v-window-item>


      <v-window-item :value="6" 
        class="no-transition" 
      >
        <v-card-text>
          <v-container>
            <v-row>
              <v-col>
                <h3
                  class="mb-4"
                >
                  Distance and angular size
                </h3>
                <div>
                  <p>
                    As with the people, if we know the physical length of a galaxy, then its angular size tells us its distance from us. 
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
                        $$ \small{\text{Galaxy's Angular Size} (\theta) = \frac{\text{Galaxy's Physical Length} (L)}{\text{Galaxy's Distance} (D)}} $$  
                      </p>
                      <h6>
                        (ask your instructor for more information if you want to know how to use trigonometry to derive this formula).
                      </h6> 
                    </v-card-text>
                  </v-card>
                </div>
              </v-col>
            </v-row>
            <v-spacer></v-spacer>
            <v-row>
              <v-col>
                <p>
                  (Anna is making a better version of this figure!)
                </p>
                <v-img
                  class="mx-a"
                  contain
                  :src="`${state.image_location}/theta_L_over_D_janky_schematic.jpg`"
                ></v-img>
              </v-col>
            </v-row>
            <p
              class="mt-4"
            >
              For galaxies that are the <strong>same physical length</strong>, the larger the distance, the smaller galaxy will appear in angular size.   
            </p>
          </v-container>
        </v-card-text>
      </v-window-item>
    

      <v-window-item :value="7" 
        class="no-transition"
      >
        <v-card-text>
          <v-container>
            <v-row>
              <v-col
                cols="7"
              >
                <div>
                  <h3
                    class="mb-4"
                  >
                    Reflect
                  </h3>
                  <v-row>                     
                    <v-card
                      class="mt-auto white--text"
                      flat
                      color="info"
                    >
                      <v-card-text 
                        v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
                      >
                        <p>
                          $$ \small{\text{Galaxy's Angular Size} (\theta) = \frac{\text{Galaxy's Physical Length} (L)}{\text{Galaxy's Distance} (D)}} $$ 
                        </p>
                      </v-card-text>
                    </v-card>
                    </v-row>
                    <v-spacer></v-spacer>
                    <v-row>
                      <p
                        class="mt-4"
                      >
                        Assume galaxies A and B in this image have the <strong>same physical length</strong>. What can you determine about their relative distances?
                      </p>
                      <!-- Whoops, is there any way to pass on the formatting info in the feedback responses without treating them as strings? -->
                      <mc-radiogroup
                        :radio-options="[
                          'Galaxy A and Galaxy B are the same distance away from us.',
                          'Galaxy A is farther away from us than Galaxy B.',
                          'Galaxy A is closer to us than Galaxy B.',
                          'We do not have enough information to answer this question'
                        ]"
                        :feedbacks="[
                          'Try again. \n Think about the people on the beach. Did the closer person appear bigger or smaller than the farther person?',
                          'Try again. \n Think about the people on the beach. Did the closer person appear bigger or smaller than the farther person?',
                          'That\'s right! The <strong>closer</strong> galaxy has a <strong>larger</strong> angular size in the sky.',
                          'Try again. \n Think about the people on the beach. Did the closer person appear bigger or smaller than the farther person?'
                        ]"
                        :correct-answers="[2]"
                        :selected-callback="(option) => { if(option.correct || option.neutral) { max_step_completed = Math.max(max_step_completed, 7); } }"
                      >
                      </mc-radiogroup>
                    </v-row>
                  </div>
                </v-col> 
                <v-col
                  cols="5"
                >
                  <h4
                    class="mb-2"
                  >
                    Galaxies in the Sky
                  </h4>
                  <v-img
                    class="mx-a"
                    contain
                    :src="`${state.image_location}/galaxies A B boxed - Harry may update with nicer boxes.png`"
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
              <v-col>
                <h3
                  class="mb-4"
                >
                  Angular Size and Distance
                </h3>
                <div>                    
                  <p>
                    Now let’s think in terms of actual numbers.
                  </p>
                  <v-col
                    cols="7"
                  >
                    <v-card
                      class="white--text"
                      flat
                      color="info"
                    >
                      <v-card-text
                        v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
                      >
                        <p>
                          $$ \small{\text{Galaxy's Angular Size} (\theta) = \frac{\text{Galaxy's Physical Length} (L)}{\text{Galaxy's Distance} (D)}} $$ 
                        </p>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-spacer></v-spacer>
                  <p>
                    This relationship tells us: if two galaxies are the same size and one is <strong>2 times</strong> farther from us as the other, the far one will have 1/2 the angular size in our sky.
                  </p>
                  <p>
                    If one galaxy is <strong>50 times</strong> farther from us as the other, the far one will have <strong>1/50</strong> the angular size in our sky, and so on.
                  </p>
                </div>
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
                cols="7"
              >
                <div>
                  <v-row>
                    <h3
                      class="mb-4"
                    >
                      Reflect
                    </h3>                           
                    <p>
                      Use the image to estimate <strong>how much</strong> closer Galaxy A is than Galaxy B. Assume galaxies A and B have the <strong>same physical length</strong>.
                    </p>
                    <v-card
                      class="mt-auto white--text"
                      flat
                      color="info"
                    >
                      <v-card-text
                        v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
                      >
                        <p>
                          $$ \small{\text{Galaxy's Angular Size} (\theta) = \frac{\text{Galaxy's Physical Length} (L)}{\text{Galaxy's Distance} (D)}} $$ 
                        </p>
                      </v-card-text>
                    </v-card>
                  </v-row>
                  <v-row>
                    <mc-radiogroup
                      :radio-options="[
                        'Galaxy A is about 2 times closer to us than Galaxy B.',
                        'Galaxy A is about 10 times closer to us than Galaxy B.',
                        'Galaxy A is about 1000 times closer to us than Galaxy B.',
                        'There is not enough information to estimate the relative distances to the galaxies.'
                      ]"
                      :feedbacks="[
                        'Try again. \n Try to imagine how many times you could lay Galaxy B across Galaxy A.',
                        'That\'s right!',
                        'Try again. \n Try to imagine how many times you could lay Galaxy B across Galaxy A.',
                        'Try again. \ You could probably fit 10 Galaxy B’s across Galaxy A.'
                      ]"
                      :correct-answers="[1]"
                      :selected-callback="(option) => { if(option.correct || option.neutral) { max_step_completed = Math.max(max_step_completed, 9); } }"
                    >
                    </mc-radiogroup>
                  </v-row>
                </div>
              </v-col> 
              <v-col
                cols="5"
              >
                <div>
                  <h4
                    class="mb-2"
                  >
                    Galaxies in the Sky
                  </h4>
                  <v-img
                    class="mx-a"
                    contain
                    :src="`${state.image_location}/galaxies A B boxed - Harry may update with nicer boxes.png`"
                  ></v-img>
                </div>
              </v-col>
            </v-row> 
          </v-container>            
        </v-card-text>
      </v-window-item>


      <v-window-item :value="10"
        class="no-transition"
      >
        <v-card-text
          v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
        >
          <v-container>
            <v-row>
              <v-col
                cols="8"
              >
                <h3
                  class="mb-4"
                >
                  Distance and Angular Size
                </h3>
                <div>
                  <p>
                    Nice work! To estimate distances to <strong>your</strong> galaxies, we start with this same formula:
                  </p>
                  <p>
                    $$ \small{\text{Galaxy's Angular Size} (\theta) = \frac{\text{Galaxy's Physical Length} (L)}{\text{Galaxy's Distance} (D)}} $$ 
                  </p>
                  <p>
                    With some algebra and unit conversions, this becomes: 
                  </p>
                  <v-card
                    class="mt-3 white--text"
                    flat
                    color="info"
                  >
                    <v-card-text
                      v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
                    >
                      <p>
                        $$ \small{\text{Galaxy Distance} =  200,000 \cdot \frac{\text{physical length of galaxy}}{\text{Galaxy’s angular size ($\theta$, in arcseconds)}}} $$
                      </p>
                    </v-card-text>
                  </v-card>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-window-item>


      <v-window-item :value="11"
        class="no-transition"
      >
        <v-card-text
          v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
        >
          <v-container>
            <v-row>
              <v-col
                cols="9"
              >
                <h3
                  class="mb-4"
                >
                  Physical Length of a Galaxy
                </h3>
                <v-card
                  class="white--text"
                  flat
                  color="info"
                >
                  <v-card-text
                    v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
                  >
                    <p>
                      $$ \small{\text{Galaxy Distance} = 200,000 \cdot \frac{\text{physical length of galaxy}}{\text{Galaxy’s angular size ($\theta$, in arcseconds)}}} $$
                    </p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-row> 
              <v-col>         
                <p>
                  This equation from the previous slide requires two pieces of information to determine the distance to a galaxy:
                  <ol>
                    <li>the <strong>physical length</strong> of the galaxy</li>
                    <li>the <strong>angular size</strong> of the galaxy</li> 
                  </ol>
                </p>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="9"
              >
                <p>
                  In this data story, we are going to make an assumption that all galaxies are the <strong>same physical length as the Milky Way galaxy</strong>:
                </p>
                <v-card
                  class="mb-3 white--text"
                  flat
                  color="info"
                >
                  <v-card-text
                    v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
                  >
                    <p>
                      $$ \text{physical length of Milky Way galaxy, }  L = 100,000 \text{ light years}  = 0.03 \text{ Mpc} $$
                    </p>
                  </v-card-text>
                </v-card>
                <p>
                  <strong>(You can ponder later whether you think this is a good or bad assumption!)</strong>
                </p>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-window-item>          


      <v-window-item :value="12"
        class="no-transition"
      >
        <v-card-text
          v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
        >
          <v-container>
            <v-row>
              <v-col>
                <h3
                  class="mb-4"
                >
                  Milky Way Length in Mpc
                </h3>
                <p>
                  When measuring very large distances, astronomers use a unit called a Megaparsec (Mpc). 
                </p>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="8"
              >
                <p>
                  If we substitute the physical length of the Milky Way in our equation, we get:
                </p>
                <v-card
                  class="mb-3 white--text"
                  flat
                  color="info"
                >
                  <v-card-text
                    v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}"
                  >
                    <p>
                      $$ \mathbf{\text{ Distance in Mpc} = \frac{6200}{ \text{galaxy angular size (}\theta \text{ in arcseconds)}}} $$
                    </p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <p>
                  So, to measure the distance to a galaxy like the Milky Way, all you have to do is measure its <strong>angular size</strong> in arcseconds. Let’s get started.
                </p>
              </v-col>
            </v-row> 
          </v-container>
        </v-card-text>    
      </v-window-item>
    </v-window>

    <v-divider></v-divider>

    <v-card-actions
      class="justify-space-between"
    >
      <v-btn
        :disabled="step === 0"
        class="black--text"
        color="accent"
        depressed
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
            :disabled="n > max_step_completed + 2"
            :input-value="active"
            icon
            @click="toggle"
          >
            <v-icon
              color="info lighten-1"
            >
              mdi-record
            </v-icon>
          </v-btn>
        </v-item>
      </v-item-group>

      <v-spacer></v-spacer>

      <v-btn
        :disabled="step > max_step_completed"
        v-if="step < length-1"
        class="black--text"
        color="accent"
        depressed
        @click="step++;"
      >
        next
      </v-btn>

      <!-- first button below just being used for testing, delete when using live with students -->
      <v-btn
        v-if="step < 12 && show_team_interface"
        color="error"
        class="black--text"
        depressed
        @click="() => {
          two_intro_complete = true;
          step = 0;
        }"
      >
        get started
      </v-btn>
      
      <v-btn
        v-if="step >= 12"
        :disabled="step > 12"
        color="accent"
        class="black--text"
        depressed
        @click="() => {
          two_intro_complete = true;
          step = 0;
        }"
      >
        get started
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
module.exports = {
  props: ["buttonText", "titleText", "closeText"],

  watch: {
    step(newStep, oldStep) {
      const isInteractStep = this.interact_steps.includes(newStep);
      const newCompleted = isInteractStep ? newStep - 1 : newStep;
      max_step_completed = Math.max(max_step_completed, newCompleted);
    },
  },
};
</script>

<style>
.no-transition {
  transition: none;
}

#slideshow-root .v-card__text{
  padding: 0px 15px 0px;
  min-height: 550px;
}
</style>
