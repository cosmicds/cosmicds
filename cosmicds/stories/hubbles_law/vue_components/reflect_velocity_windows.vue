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
            {{ currentTitle }}
          </span>
          <span
            @click="() => { dialog = false; if (step == 6)  {step = 0}; }"
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
              How do the observed wavelengths of emission or absorption lines in your galaxies
              compare with the “rest” wavelength of those lines?
              <mc-radiogroup
                :radio-options="[
                  'Lines in the galaxies have the same wavelength as the lines at rest.',
                  'Some galaxies have lines with smaller wavelengths and some have lines with larger wavelengths than the lines at rest.',
                  'Most or all of the galaxies have lines with smaller wavelengths than the lines at rest.',
                  'Most or all of the galaxies have lines with larger wavelengths than the lines at rest.'
                ]"
                :feedbacks="['Try again.', 'Try again.', 'Try again.', 'That\'s right!']"
                :answer-key="3"
              >
              </mc-radiogroup>
            </v-card-text>
          </v-window-item>


          <v-window-item :value="3"
            class="no-transition"
          >
            <v-card-text>
              From the data you just collected, what can you conclude about how the galaxies are moving relative to our home galaxy, the Milky Way?
              <mc-radiogroup
                :radio-options="[
                  'The galaxies are not moving.',
                  'Some galaxies are moving toward our galaxy and some galaxies are moving away from our galaxy.',
                  'Galaxies are mostly moving toward our galaxy.',
                  'Galaxies are mostly moving away from our galaxy.'
                ]"
                :feedbacks="['Try again.', 'Try again.', 'Try again.', 'That\'s right!']"
                :answer-key="3"
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
                :answer-key="1"
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
                :answer-key="2"
              >
              </mc-radiogroup>
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
                Nice work reflecting!
              </h3>
              <span class="text-caption grey--text">You can start plotting your data now.</span>
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
            @click="() => { $emit('submit'); dialog = false; step = 0; }"
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
        case 0: return "Reflect on your Data"
        case 1: return "What would a 1920's Scientist Wonder?" 
        case 2: return "Observed vs. Rest Wavelengths"
        case 3: return "How Galaxies Move"  
        case 4: return "Do Data Agree with 1920's Thinking?"
        case 5: return "Do Data Agree with 1920's Thinking?"
        default: return "Complete"
      }
    },
  },
};
</script>
