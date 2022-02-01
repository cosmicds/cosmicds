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
            @click="() => { dialog = false; if (step == 8)  {step = 1}; }"
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
        >
          <v-window-item :value="1">
            <v-card-text>
              How do the observed wavelengths of emission or absorption lines in your galaxies
              compare with the “rest” wavelength of those lines?
              <mc-radiogroup
                radio-one="Lines in the galaxies have the same wavelength as the lines at rest."
                radio-two="Some galaxies have lines with smaller wavelengths and some have lines with larger wavelengths than the lines at rest."
                radio-three="Most or all of the galaxies have lines with smaller wavelengths than the lines at rest."
                radio-four="Most or all of the galaxies have lines with larger wavelengths than the lines at rest."
                answer-key=4
                color-one="red"
                color-two="red"
                color-three="red"
                color-four="green"
                feedback-one="Try again."
                feedback-two="Try again."
                feedback-three="Try again."
                feedback-four="That's right!"
              >
              </mc-radiogroup>
            </v-card-text>
          </v-window-item>


          <v-window-item :value="2">
            <v-card-text>
              From the data you just collected, what can you conclude about how the galaxies are moving relative to our home galaxy, the Milky Way?
              <mc-radiogroup
                radio-one="The galaxies are not moving."
                radio-two="Some galaxies are moving toward our galaxy and some galaxies are moving away from our galaxy."
                radio-three="Galaxies are mostly moving toward our galaxy."
                radio-four="Galaxies are mostly moving away from our galaxy."
                answer-key=4
                color-one="red"
                color-two="red"
                color-three="red"
                color-four="green"
                feedback-one="Try again."
                feedback-two="Try again."
                feedback-three="Try again."
                feedback-four="That's right!"
              >
              </mc-radiogroup>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="3">
            <v-card-text>
              These were the prevailing viewpoints in the 1920's:
              <ul class="mb-4">  
                <li><em>The universe is static and unchanging</em></li>
                <li><em>Galaxies in the universe are moving randomly</em></li>
              </ul>
              <h3>Question 1</h3>
              Do your data support either of these conclusions?
              <form-textarea
                question-label="Question 1"
              >
              </form-textarea>
              <h3>Question 2</h3>
              What would you tell a scientist from 1920 regarding the prevailing wisdom about galaxies during this time?
              <form-textarea
                question-label="Question 2"
              >
              </form-textarea>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="4">
            <v-card-text>
              These were the prevailing viewpoints in the 1920's:
              <ul class="mb-4">  
                <li><em>The universe is static and unchanging</em></li>
                <li><em>Galaxies in the universe are moving randomly</em></li>
              </ul>
              <h3>Question 3</h3>
              Based on your data, how confident are you about what you told the 1920's scientist? What would improve your confidence in your data and conclusions?
              <form-textarea
                question-label="Question 3"
              >
              </form-textarea>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="5">
            <v-card-text>
              <p>
                You concluded from your data that your galaxies seem to be moving AWAY from our Milky Way galaxy.
              </p>
              <p>
                The Doppler equation can be used to figure out just how fast the galaxies are moving.
              </p>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="6">
            <v-card-text>
              MATHJAX Stuff
            </v-card-text>
          </v-window-item>

          <v-window-item :value="7">
            <v-card-text>
              <p>
                Great, notice your calculated velocity is now entered in the table.
              </p>
              <p>
                Now that you know how to use this equation, click below to have the velocities of the remaining galaxies calculated as well.
              </p>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="8">
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
            color="accent"
            text
            @click="step--"
          >
            Back
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            :disabled="step === 8"
            color="accent"
            text
            @click="step++;"
          >
            {{ step < 8 ? 'next' : '' }}
          </v-btn>
          <v-btn
            :disabled="step < 8"
            color="accent darken-1"
            depressed
            @click="() => { $emit('submit'); dialog = false; step = 1; }"
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
        case 1: return "Observed vs. Rest Wavelengths"
        case 2: return "How Galaxies Move"
        case 3: return "Feedback for a 1920's Scientist"
        case 4: return "Confidence in Your Conclusions"
        case 5: return "Moving Away"
        case 6: return "MATHJAX"
        case 7: return "Remaining Galaxy Velocities"
        default: return "Complete"
      }
    },
  },
};
</script>