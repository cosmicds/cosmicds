<template>
  <v-btn
    block
    color="info"
    elevation="2"
    @click.stop="dialog = true"
  >
    <v-spacer></v-spacer>
    {{ buttonText }}
    <v-spacer></v-spacer>
    <v-icon
      class="ml-4"
    >
      {{ reflection_complete ? 'mdi-check-circle-outline' : 'mdi-circle-outline' }}
    </v-icon>

    <v-dialog
        v-model="dialog"
        persistent
        max-width="800px"
    >
      <v-card
        class="mx-auto"
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
          <v-spacer></v-spacer>
          <!-- @click="() => { dialog = false; if (step == 7)  {step = 0}; }" -->
          <span
            @click="() => { $emit('submit'); dialog = false; reflection_complete = true}"
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
          vertical
          style="height: 60vh;"
          class="overflow-auto"
        >
          <v-window-item :value="0" 
            class="no-transition"
          >
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col>
                    <p>
                      Throughout this reflection sequence, you will answer questions that are designed to guide your thinking. Your responses will be recorded (as in a scientist’s lab notebook), so that you can use this information to support your claims later in this Data Story.
                    </p>
                    <p>
                      Scientists do not work in a vacuum and neither should you. You can consult colleagues (i.e. classmates or lab partners) and instructors for help.
                    </p>
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
                    <p>
                      Recall that you are looking at the same kind of observations Vesto Slipher made in 1920. We’ll ask you some questions about your data that astronomers in 1920 might have asked about Slipher’s data.
                    </p>
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
                  <v-col>
                    <p>
                      How do the observed wavelengths of your galaxies' spectral lines compare with their rest wavelengths?
                    </p>
                    <p>
                      Choose the best response below. (Note: You can grab this pop-up by the header and move it to the side if you want to see content behind it.)
                    </p>
                    <mc-radiogroup
                      :radio-options="[
                        'In ALL of my galaxies, the observed wavelengths of the spectral lines are the SAME as the rest wavelengths.',
                        'In ALL of my galaxies, the observed wavelengths of the spectral lines are LONGER than the rest wavelengths.',
                        'In ALL of my galaxies, the observed wavelengths of the spectral lines are SHORTER than the rest wavelengths.',
                        'In SOME of my galaxies, the observed wavelengths of the spectral lines are LONGER than the rest wavelengths. In OTHER of my galaxies, the observed wavelengths of the spectral lines are SHORTER than the rest wavelengths.'
                      ]"
                      :feedbacks="[
                        'Try again. For each galaxy (a row in the table), compare the values for rest wavelength (column 3) and observed wavelength (column 4).',
                        'That is correct.',
                        'Try again. For each galaxy (a row in the table), compare the values for rest wavelength (column 3) and observed wavelength (column 4).',
                        'Try again. For each galaxy (a row in the table), compare the values for rest wavelength (column 3) and observed wavelength (column 4).'
                      ]"
                      :correct-answers="[1]"
                      :selected-callback="(state) => { if(state.correct) { max_step_completed = Math.max(max_step_completed, 2); } }"
                      score-tag="wavelength-comparison"
                    >
                    </mc-radiogroup>
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
                    <p>
                      From the data you have collected so far, what can you conclude about how your observed galaxies are moving relative to our home galaxy, the Milky Way?
                    </p>
                    <p>
                      Choose the best response below.
                    </p>
                    <mc-radiogroup
                      :radio-options="[
                        'My observed galaxies are NOT moving relative to our galaxy.',
                        'All of my observed galaxies are moving AWAY from our galaxy.',
                        'All of my observed galaxies are moving TOWARD our galaxy.',
                        'Some of my observed galaxies are moving AWAY from our galaxy, and some galaxies are moving TOWARD our galaxy.'
                      ]"
                      :feedbacks="[
                        'Try again. Recall that when the observed wavelength is LONGER than the rest wavelength, this indicates motion AWAY from the observer.',
                        'That is correct.',
                        'Try again. Recall that when the observed wavelength is LONGER than the rest wavelength, this indicates motion AWAY from the observer.',
                        'Try again. Recall that when the observed wavelength is LONGER than the rest wavelength, this indicates motion AWAY from the observer.'
                      ]"
                      :correct-answers="[1]"
                      :selected-callback="(state) => { if(state.correct) { max_step_completed = Math.max(max_step_completed, 3); } }"
                      score-tag="galaxy-motion"
                    >
                    </mc-radiogroup>
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
                    <p>
                      You concluded from your data that all five of your galaxies seem to be <strong>moving away</strong> from our Milky Way galaxy. 
                    </p>
                    <p>
                      Remember that the dominant view in the 1920’s is that the universe is <strong>static</strong> and <strong>unchanging</strong>. Are your data consistent with this model of the universe?
                    </p>
                    <mc-radiogroup
                      :radio-options="[
                        'Yes.',
                        'No.',
                        'I am not sure.'
                      ]"
                      :feedbacks="[
                        'Actually, your evidence does not support this statement. Galaxies would not be moving in a universe that is static and unchanging.',
                        'That\'s right.',
                        'You <strong>can</strong> draw a conclusion about this statement based on your evidence. Consider this and try again: galaxies would not be moving in a universe that is static and unchanging. And you have already concluded that your observed galaxies are moving. So...'
                      ]"
                      :correct-answers="[1]"
                      :neutral-answers="[2]"
                      :selected-callback="(state) => { if(state.correct || state.neutral) { max_step_completed = Math.max(max_step_completed, 4); } }"  
                      score-tag="steady-state-consistent"
                    >
                    </mc-radiogroup>
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
                    <p>
                      An alternate hypothesis of the 1920's is that galaxies in the universe are <strong>moving randomly</strong>.
                    </p>
                    <p>
                      Are your data consistent with this model of the universe?
                    </p>
                    <mc-radiogroup
                      :radio-options="[
                        'Yes.',
                        'No.',
                        'I am not sure.'
                      ]"
                      :feedbacks="[
                        'With only 5 galaxies, it is difficult to draw strong conclusions about the motion of galaxies. However, note that your galaxies all seem to be moving in the same direction (away from us). If galaxies move randomly, you would expect some to be moving toward us and some to be moving away.',
                        'Your galaxies all seem to be moving in the same direction (away from us), which is NOT consistent with galaxies that move randomly. However, it may be difficult to say for sure with data from only 5 galaxies.',
                        'That\'s fair. With only 5 galaxies, it is difficult to draw strong conclusions about the motion of galaxies. However, note that your galaxies all seem to be moving in the same direction (away from us). If galaxies move randomly, you would expect some to be moving toward us and some to be moving away.'
                      ]"
                      :neutral-answers='[0,1,2]'
                      :selected-callback="(state) => { if(state.neutral) { max_step_completed = Math.max(max_step_completed, 5); } }" 
                      score-tag="moving-randomly-consistent"
                    >
                    </mc-radiogroup>
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
                <v-row>
                  <v-col>
                    <p>
                      You have looked at the spectra for only 5 galaxies. It might give you more confidence if you pool your data with others, so that you can draw conclusions from a larger number of galaxies.
                    </p>
                    <p>
                      Take a minute to talk with your peers. Do their data agree or disagree with yours? 
                    </p>
                    <mc-radiogroup
                      :radio-options="[
                        'Their data agree with mine. Their galaxies are also moving away from us.',
                        'Their data disagree with mine. Their galaxies are not all moving away from us.',
                        'I am working on my own and do not have someone to check with.'
                      ]"
                      :feedbacks="[
                        'Interesting that they also got the same result as you. Does that give you more confidence in your conclusions?',
                        'Hmm. That is an unexpected result. It might be helpful to check in with your instructor.',
                        'No problem. Checking the Cosmic Data Stories database, everyone else who has completed this story also found that their galaxies are all moving away from us. Does that give you more confidence in your conclusions?']"
                      :neutral-answers="[0,2]"
                      :selected-callback="(state) => { if(state.correct || state.neutral) { max_step_completed = Math.max(max_step_completed, 6); } }" 
                      score-tag="peers-data-agree"
                    >
                    </mc-radiogroup>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>         


          <v-window-item :value="7"
            class="no-transition"
            style="height: 100%;"
          >
            <v-card-text
              style="height: 100%;"
            >
              <v-container
                style="height: 100%;"
              >
                <v-row
                  style="height: 100%;"
                  align="center"
                >
                  <v-col
                    class="pa-4 text-center my-auto"
                  >
                    <v-img
                      class="mb-4"
                      contain
                      height="128"
                      src="https://www.pngrepo.com/png/211744/512/rocket-ship-launch-missile.png"
                    ></v-img>
                    <h3 class="text-h6 font-weight-light mb-2">
                      Nice work reflecting!
                    </h3>
                    <span class="text-caption grey--text">You can start calculating velocities now.</span>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-window-item>
        </v-window>

        <v-divider></v-divider>

        <v-card-actions>
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
            <!-- vue's v-for with a range starts the count at 1, so we have to add 2 in the disabled step instead of 1 to account for the fact that we are otherwise counting the windows from 0 https://v2.vuejs.org/v2/guide/list.html?redirect=true#v-for-with-a-Range-->
              <v-btn
                :disabled="n > max_step_completed + 2"
                :input-value="active"
                icon
                @click="toggle"
              >
                <v-icon
                  color="info"
                >
                  mdi-record
                </v-icon>
              </v-btn>
            </v-item>
          </v-item-group>
          <v-spacer></v-spacer>
          <v-btn
            v-if="step < 7"
            :disabled="step > max_step_completed"
            class="black--text"
            color="accent"
            depressed
            @click="step++;"
          >
            Next
          </v-btn>
          <v-btn
            v-if="step >= 7"
            color="accent"
            class="black--text"
            depressed
            @click="() => { $emit('submit'); dialog = false; step = 0; reflection_complete = true}"
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
      length: 8,
      dialog: false,
      max_step_completed: 0,
      interact_steps: [2,3,4,5,6],
      reflection_complete: false
    };
  },
  computed: {
    currentTitle () {
      switch (this.step) {
        case 0: return "Reflect on your data"
        case 1: return "What would a 1920's scientist wonder?" 
        case 2: return "Observed vs. rest wavelengths"
        case 3: return "How galaxies move"  
        case 4: return "Do your data agree with 1920's thinking?"
        case 5: return "Do your data agree with 1920's thinking?"
        case 6: return "Did your peers find what you found?"
        default: return "Reflection complete"
      }
    },
  },
  watch: {
    step(newStep, oldStep) {
        const isInteractStep = this.interact_steps.includes(newStep);
        const newCompleted = isInteractStep ? newStep - 1 : newStep;
        this.max_step_completed = Math.max(this.max_step_completed, newCompleted)
    }
  }
};
</script>
