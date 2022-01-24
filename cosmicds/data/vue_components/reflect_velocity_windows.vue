<template>
  <v-btn
  block
      color="accent"
      class="black--text"
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
          <span>{{ currentTitle }}</span>
          <v-avatar
            color="info"
            class="subheading white--text"
            size="24"
            v-text="step"
          ></v-avatar>
        </v-card-title>


        <v-window
          v-model="step"
          vertical
        >
        <!--
          <v-window-item :value="1">
            <v-card-text>
              How do the observed wavelengths of emission or absorption lines in your galaxies
              compare with the “rest” wavelength of those lines?
              <mc-radiogroup
                radio-one="Lines in the galaxies have the same wavelength as the lines at rest."
                radio-two="Some galaxies have lines with smaller wavelengths and some have lines with larger wavelengths than the lines at rest."
                radio-three="Most or all of the galaxies have lines with smaller wavelengths than the lines at rest."
                radio-four="Most or all of the galaxies have lines with larger wavelengths than the lines at rest."
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
              >
              </mc-radiogroup>
            </v-card-text>
          </v-window-item>
          -->
          <v-window-item :value="4">
            <v-card-text v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}">
            <p>
              Step 1: We will use the Doppler equation, which relates the observed wavelength of your spectral lines to their rest wavelength as follows:
            </p>
            <p>
              $$ v=c \left(\frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}}-1\right) $$
              $$ v\text{: velocity of your galaxy, in km/s}$$ 
              $$ c\text{: speed of light, 300,000 km/s}$$
              $$ \lambda_{\text{obs}}\text{: observed wavelength of spectral line in your galaxy} $$
              $$ \lambda_{\text{rest}}\text{: rest wavelength of spectral line} $$
            </p>

            <p>
              Step 2: Click on a row of your table to choose one of your galaxies and calculate its velocity. 
            </p>
            <p>
              (highlight row in table)
            </p>

            <p>
              Step 3: Enter the observed and rest wavelengths of your spectral line into the cells in the equation below:
            </p>
            <p>
              $$ v=c \left(\frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}}-1\right) = c \left(\frac{\bbox[DarkSlateGrey]{\input[lam_obs][]{}}}{\bbox[DarkSlateGrey]{\input[lam_rest][]{}}}-1\right)  $$
            </p>
          </v-window-item>

          <v-window-item :value="5">
            <v-card-text v-intersect="(entries, _observer, intersecting) => { if (intersecting) { MathJax.typesetPromise(entries.map(entry => entry.target)) }}">
            <p>
              Step 4: (Can't get here until values in Step 3 are entered correctly)
            </p>
            <p>
              $$ v=c \left(\frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}}-1\right) = c \left(\frac{\bbox[DarkSlateGrey]{\text{this should display student's value of lam_obs}}}{\bbox[DarkSlateGrey]{\text{this should display student's value of lam_rest}}}-1\right) = c \left(\bbox[DarkSlateGrey]{\input[ratio_lam][]{}}-1\right)  $$
            </p>
          </v-window-item>



<!--
              <v-row>
                <v-col cols = 6>
                </v-col>
                <v-col cols = 6>
                  <v-row>
                    <v-col cols = "5">
                      <v-text-field
                        label="observed wavelength"
                        outlined
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols = "2"
                      class="text-center"
                    >
                      -
                    </v-col>
                    <v-col cols = "5">
                      <v-text-field
                        label="rest wavelength"
                        outlined
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                      <v-divider class="mb-2"></v-divider>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols = "12">
                      <v-text-field
                        label="rest wavelength"
                        outlined
                      ></v-text-field>
                    </v-col>
                  </v-row>

                  <v-row>
                    <v-col cols = "12">
                      <v-text-field
                        label="observed - rest"
                        outlined
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                      <v-divider class="mb-2"></v-divider>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols = "12">
                      <v-text-field
                        label="rest wavelength"
                        outlined
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-col>
              </v-row>
            </v-card-text>

          </v-window-item>

          <v-window-item :value="4">
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
-->

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
            :disabled="step === 5"
            color="accent"
            text
            @click="step++;"
          >
            {{ step < 5 ? 'next' : '' }}
          </v-btn>
          <v-btn
            :disabled="step < 5"
            color="accent darken-1"
            depressed
            @click="() => { $emit('close'); dialog = false; }"
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
        case 1: return 'Observed vs. Rest Wavelengths'
        case 2: return 'How Galaxies Move'
        case 3: return 'Calculate Galaxy Velocity'
        default: return 'Complete'
      }
    },
  },
};
</script>