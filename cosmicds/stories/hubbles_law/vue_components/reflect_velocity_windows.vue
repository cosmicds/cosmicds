<template>
  <v-btn
    block
    color="info"
    elevation="2"
    @click.stop="dialog = true"
  >
    {{ buttonText }}
    <v-icon
      class="ml-4"
    >
      {{ reflection_completed ? 'mdi-check-circle-outline' : 'mdi-circle-outline' }}
    </v-icon>

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
            {{ currentTitle }}
          </span>
          <span
            @click="() => { dialog = false; if (step == 7)  {step = 0}; }"
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
          vertical
          class="no-transition"
          style="min-height: 400px;"
        >
          <v-window-item :value="0" 
            class="no-transition"
          >
            <v-card-text>
              <p>
                Throughout the data story, you will answer questions that are designed to guide your thinking. Your responses will be recorded (as in a scientist’s lab notebook), so you can use this information to support your claims later in the story.
              </p>
              <p>
                Scientists do not work in a vacuum and neither should you. You can consult colleagues (classmates or lab partners) and instructors for help.
              </p>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="1" 
            class="no-transition"
          >
            <v-card-text>
              <p>
                Recall that you are looking at the same kind of observations Vesto Slipher made in 1920. We’ll ask you some of the question astronomers in 1920 might have asked about Slipher’s data.
              </p>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="2" 
            class="no-transition"
          >
            <v-card-text>
              <p>
                How do the observed wavelengths of your galaxies' spectral lines compare with their rest wavelengths? Choose the response that best completes the sentence below.
              </p>
              <em>The observed wavelengths of the spectral lines...:</em>
              <mc-radiogroup
                :radio-options="[
                  'in ALL of my galaxies are the SAME as the rest wavelengths of the lines.',
                  'in SOME of my galaxies are LONGER than the rest wavelengths of the lines and are SHORTER in other galaxies.',
                  'in ALL of my galaxies are LONGER than the rest wavelengths of the lines.',
                  'in ALL of my galaxies are SHORTER than the rest wavelengths of the lines.',
                ]"
                :feedbacks="['Try again. For each galaxy (a row in the table), compare the values for rest wavelength (column 3) and observed wavelength (column 4).', 'Try again. For each galaxy (a row in the table), compare the values for rest wavelength (column 3) and observed wavelength (column 4).', 'That is correct.', 'Try again. For each galaxy (a row in the table), compare the values for rest wavelength (column 3) and observed wavelength (column 4).']"
                :correct-answers="[2]"
                :selected-callback="(index) => { if([2].includes(index)) { this.max_step_completed = Math.max(this.max_step_completed, 2); } }"
              >
              </mc-radiogroup>
            </v-card-text>
          </v-window-item>


          <v-window-item :value="3"
            class="no-transition"
          >
            <v-card-text>
              From the data you just collected, what can you conclude about how your observed galaxies are moving relative to our home galaxy, the Milky Way?
              <mc-radiogroup
                :radio-options="[
                  'My observed galaxies are not moving.',
                  'Some of my observed galaxies are moving AWAY from our galaxy and some galaxies are moving TOWARD our galaxy.',
                  'All my observed galaxies are moving AWAY from our galaxy.',
                  'All my observed galaxies are moving TOWARD our galaxy.'
                ]"
                :feedbacks="['Try again. Recall that when the observed wavelength is LONGER than the rest wavelength, this indicates motion AWAY from the observer.', 'Try again. Recall that when the observed wavelength is LONGER than the rest wavelength, this indicates motion AWAY from the observer.', 'That is correct.', 'Try again. Recall that when the observed wavelength is LONGER than the rest wavelength, this indicates motion AWAY from the observer.']"
                :correct-answers="[2]"
                :selected-callback="(index) => { if([2].includes(index)) { this.max_step_completed = Math.max(this.max_step_completed, 3); } }"  
              >
              </mc-radiogroup>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="4"
            class="no-transition"
          >
            <v-card-text>
              <p>
                You concluded from your data that all five of your galaxies seem to be moving AWAY from our Milky Way galaxy. 
              </p>

              <p>
                Are your data consistent with this 1920’s views of the universe?
              </p>

              <em>The universe is static and unchanging</em>:
              <mc-radiogroup
                :radio-options="[
                  'Yes.',
                  'No.',
                  'I am not sure.'
                ]"
                :feedbacks="['Actually, your evidence does not support this statement. Galaxies would not be moving in a universe that is static and unchanging.', 'That\'s right.', 'Your evidence does not support this statement. Galaxies would not be moving in a universe that is static and unchanging']"
                :correct-answers="[1]"
                :neutral-answers="[2]"
                :selected-callback="(index) => { if([1,2].includes(index)) { this.max_step_completed = Math.max(this.max_step_completed, 4); } }"  
              >
              </mc-radiogroup>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="5"
            class="no-transition"
          >
            <v-card-text>
              <p>
                Are your data consistent with this 1920’s views of the universe?
              </p>
              <em>Galaxies in the universe are moving randomly</em>:
              <mc-radiogroup
                :radio-options="[
                  'Yes.',
                  'No.',
                  'I am not sure.'
                ]"
                :feedbacks="['With only 5 galaxies, it may be hard to say, but your galaxies all seem to be moving in the same direction (away from us). If galaxies move randomly, you would expect some to be moving toward us and some to be moving away.', 'Your galaxies all seem to be moving in the same direction (away from us), which is NOT consistent with galaxies that move randomly, but it may be difficult to say for sure with data from only 5 galaxies.', 'With only 5 galaxies it is difficult to draw strong conclusions about the motion of galaxies, but all your data so far seem to show that the motion of galaxies is NOT random.']"
                :neutral-answers='[0,1,2]'
                :selected-callback="(index) => { if([0,1,2].includes(index)) { this.max_step_completed = Math.max(this.max_step_completed, 5); } }" 
              >
              </mc-radiogroup>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="6"
            class="no-transition"
          >
            <v-card-text>
              <p>
                You have looked at spectra for only 5 galaxies. It might give you more confidence if you pool your data with others, so you are drawing conclusions from a larger number of galaxies.
              </p>
              <p>
                Take a minute to talk with your peers. Do their data agree or disagree with yours? 
              </p>
              <mc-radiogroup
                :radio-options="[
                  'Agree. Their galaxies are also moving away from us.',
                  'Disagree. Their galaxies are not all moving away from us.',
                  'I am working on my own and do not have someone to check with.'
                ]"
                :feedbacks="['Interesting that they also got the same result as you. Does that give you more confidence in your conclusions?', 'Hmm. That is an unexpected result. It might be helpful to check in with your instructor.', 'That\'s ok. From checking the Cosmic Data Stories database, I can tell you that everyone else who has completed this story also found that their galaxies are all moving away from us.']"
                :correct-answers="[0,2]"
                :selected-callback="(index) => { if([0,2].includes(index)) { this.max_step_completed = Math.max(this.max_step_completed, 6); } }" 
              >
              </mc-radiogroup>
            </v-card-text>
          </v-window-item>         

          <v-window-item :value="7"
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
                Nice work reflecting!
              </h3>
              <span class="text-caption grey--text">You can start calculating velocities now.</span>
            </div>
          </v-window-item>
        </v-window>

        <v-divider></v-divider>

        <v-card-actions>
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
            <!-- vue's v-for with a range starts the count at 1, so we have to add 2 in the disabled step instead of 1 to account for the fact that we are otherwise counting the windows from 0 https://v2.vuejs.org/v2/guide/list.html?redirect=true#v-for-with-a-Range-->
              <v-btn
                :disabled="n > max_step_completed + 2"
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
            :disabled="step > max_step_completed"
            color="accent"
            text
            @click="step++;"
          >
            {{ step < 7 ? 'next' : '' }}
          </v-btn>
          <v-btn
            :disabled="step < 7"
            color="accent"
            class="black--text"
            depressed
            @click="() => { $emit('submit'); dialog = false; step = 0; reflection_completed = true}"
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
      reflection_completed: false
    };
  },
  computed: {
    currentTitle () {
      switch (this.step) {
        case 0: return "Reflect on your Data"
        case 1: return "What would a 1920's Scientist Wonder?" 
        case 2: return "Observed vs. Rest Wavelengths"
        case 3: return "How Galaxies Move"  
        case 4: return "Do Data Agree with 1920's Thinking?"
        case 5: return "Do Data Agree with 1920's Thinking?"
        case 6: return "Did your peers find what you found?"
        default: return "Complete"
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