<template>
    <v-dialog
        v-model="state.doppler_calc_dialog"
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
            @click="() => { state.doppler_calc_dialog = false; if (step == length)  {step = 0}; }"
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
            <v-card-text
              v-intersect="(entries, _observer, intersecting) => {
                if (!intersecting) return;
                const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
                MathJax.typesetPromise(targets);
            }">
              <p>
                Great! Now let's give ourselves some more space to work.
              </p>
              <v-card color="info" class="pa-3">
                <p class="pb-3 font-weight-medium" >
                  Click calculate to compute the value of the fraction you entered. <br>
                </p>
                $$ v=c \left(\frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}}-1\right) = c \left(\frac{\textcolor{black}{\colorbox{LightSteelBlue}{ {{ state.lambda_obs }} }} \text{ &#8491;}}{\textcolor{black}{\colorbox{LightSteelBlue}{ {{ state.lambda_rest }} }} \text{ &#8491;}}-1\right) $$ 
              </v-card>
              <v-divider role="presentation"></v-divider>
              <p class="pt-5 font-weight-light">
                \(v\): velocity of your galaxy, in km/s <br>
                \(c\): speed of light, 300,000 km/s <br>
                \(\lambda_{\text{obs}}\): observed wavelength of spectral line in your galaxy <br>
                \(\lambda_{\text{rest}}\): rest wavelength of spectral line} <br>
              </p>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="1"
            class="no-transition"
          >
            <v-card-text v-intersect="(entries, _observer, intersecting) => {
              if (!intersecting) return;
              const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
              MathJax.typesetPromise(targets);
            }">
                $$ v=c \left(\frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}}-1\right) = c \left(\frac{\textcolor{black}{\colorbox{LightSteelBlue}{ {{ state.lambda_obs }} }} \text{ &#8491;}}{\textcolor{black}{\colorbox{LightSteelBlue}{ {{ state.lambda_rest }} }} \text{ &#8491;}}-1\right) $$ 
              <p>
                Dividing the fraction gives you:
              </p>
              <v-card color="info" class="pa-3">
                $$ v= c\left(\textcolor{black}{\colorbox{LightSteelBlue}{ {{ (state.lambda_obs/state.lambda_rest).toFixed(5)}} } } -1 \right) $$
                <p class="pt-3 font-weight-medium" >  
                  Click calculate again to perform the subtraction.
                </p>
              </v-card>
              <v-divider role="presentation"></v-divider>
              <p class="pt-5 font-weight-light">
                \(v\): velocity of your galaxy, in km/s <br>
                \(c\): speed of light, 300,000 km/s <br>
                \(\lambda_{\text{obs}}\): observed wavelength of spectral line in your galaxy <br>
                \(\lambda_{\text{rest}}\): rest wavelength of spectral line} <br>
              </p>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="2"
            class="no-transition"
          >
            <v-card-text v-intersect="(entries, _observer, intersecting) => {
              if (!intersecting) return;
              const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
              MathJax.typesetPromise(targets);
            }">
              <p>
                $$ v=c \left(\frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}}-1\right) = c \left(\frac{\textcolor{black}{\colorbox{LightSteelBlue}{ {{ state.lambda_obs }} }} \text{ &#8491;}}{\textcolor{black}{\colorbox{LightSteelBlue}{ {{ state.lambda_rest }} }} \text{ &#8491;}}-1\right) $$ 

                $$ v= c\left(\textcolor{black}{\colorbox{LightSteelBlue}{ {{(state.lambda_obs/state.lambda_rest).toFixed(5)}} } } -1 \right) $$
              </p>
              <p>
                Now we are left with:
              </p>
              <v-card color="info" class="pa-3">
                $$ v=c \left(\textcolor{black}{\colorbox{LightSteelBlue}{ {{(state.lambda_obs/state.lambda_rest-1).toFixed(5)}} } } \right) $$
              </v-card>
              <v-divider role="presentation"></v-divider> 
              <p class="pt-5 font-weight-light"> 
                \(v\): velocity of your galaxy, in km/s <br>
                \(c\): speed of light, 300,000 km/s <br>
                \(\lambda_{\text{obs}}\): observed wavelength of spectral line in your galaxy <br>
                \(\lambda_{\text{rest}}\): rest wavelength of spectral line} <br>
              </p>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="3"
            class="no-transition"
          >
            <v-card-text v-intersect="(entries, _observer, intersecting) => {
              if (!intersecting) return;
              const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
              MathJax.typesetPromise(targets);
            }">
              <v-card color="info" class="pa-1">
                $$ v=c \left(\textcolor{black}{\colorbox{LightSteelBlue}{ {{(state.lambda_obs/state.lambda_rest-1).toFixed(5)}} } } \right) $$
              </v-card>
              <p class="pt-6">
                Reflect for a bit on what this means. How does the velocity of your galaxy relate to the speed of light?
              </p>
              <mc-radiogroup
                :radio-options="[
                  'There is no relationship between my galaxy\’s velocity and the speed of light.',
                  'My galaxy\’s velocity is a fraction of the speed of light. ',
                  'My galaxy\’s velocity is greater than the speed of light.'
                ]"
                :feedbacks="['Try again. The equation describes a relationship between your galaxy\’s velocity and the speed of light.', 'Correct. The fraction is the ratio of the observed wavelength of my spectral line over the line’s rest wavelength minus 1. This will be the case for all of your galaxies.', 'Try again. You are multiplying the speed of light by a value that is smaller than 1.']"
                :correct-answers="[1]"
                :selected-callback="(index) => { if([1].includes(index)) { this.maxStepCompleted5 = Math.max(this.maxStepCompleted5, 3); } }"  
              >
              </mc-radiogroup>
              <v-divider role="presentation"></v-divider> 
              <p class="pt-5 font-weight-light">
                \(v\): velocity of your galaxy, in km/s <br>
                \(c\): speed of light, 300,000 km/s <br>
                \(\lambda_{\text{obs}}\): observed wavelength of spectral line in your galaxy <br>
                \(\lambda_{\text{rest}}\): rest wavelength of spectral line} <br>
              </p>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="4"
            class="no-transition"
          >
            <v-card-text v-intersect="(entries, _observer, intersecting) => {
              if (!intersecting) return;
              const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
              MathJax.typesetPromise(targets);
            }">
              <div
                v-if="!failedValidation5"
                class="pb-5">
                Now enter the speed of light in km/s in the box below.<br> 
                Click calculate to multiply through and obtain the speed of your galaxy.
              </div>
              <div
                v-if="failedValidation5"
                class="pb-5"
              >
                Try again, check that you are using <b>km</b>/s, and make sure you have the correct number of zeroes. The speed of light is highlighted in yellow.
              </div>
              <v-card color="info" class="pa-3">
                $$ v=c \left(\textcolor{black}{\colorbox{LightSteelBlue}{ {{(state.lambda_obs/state.lambda_rest-1).toFixed(5)}} } } \right) $$
                $$ v = \bbox[DarkSlateGrey]{\input[speed_light][]{}} \text{ km/s} \times \textcolor{black}{\colorbox{LightSteelBlue}{ {{(state.lambda_obs/state.lambda_rest-1).toFixed(5)}} } } $$
              </v-card>
              <v-divider role="presentation"></v-divider>
              <div v-if="!failedValidation5">
                <p class="pt-5 font-weight-light">
                  \(v\): velocity of your galaxy, in km/s <br>
                  \(c\): speed of light, 300,000 km/s <br>
                  \(\lambda_{\text{obs}}\): observed wavelength of spectral line in your galaxy <br>
                  \(\lambda_{\text{rest}}\): rest wavelength of spectral line} <br>
                </p>
              </div>
              <div 
                v-if="failedValidation5"
                v-intersect="(entries, _observer, intersecting) => {
                  if (!intersecting) return;
                  const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
                  MathJax.typesetPromise(targets);
                }"
              >
                <p class="pt-5 font-weight-light">
                  \(v\): velocity of your galaxy, in km/s
                <p>
                <p class="yellow--text font-weight-medium" >
                  \(c\): speed of light, 300,000 km/s
                </p>
                <p class="font-weight-light">               
                  \(\lambda_{\text{obs}}\): observed wavelength of spectral line in your galaxy<br>
                  \(\lambda_{\text{rest}}\): rest wavelength of spectral line} 
                </p>
              </div>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="5"
            class="no-transition"
          >
            <v-card-text v-intersect="(entries, _observer, intersecting) => {
              if (!intersecting) return;
              const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
              MathJax.typesetPromise(targets);
            }">
              $$ v=c \left(\textcolor{black}{\colorbox{LightSteelBlue}{ {{(state.lambda_obs/state.lambda_rest-1).toFixed(5)}} } } \right) $$
              $$ v = \textcolor{black}{\colorbox{LightSteelBlue}{ {{ studentc.toLocaleString() }} } }  \text{ km/s} \times \textcolor{black}{\colorbox{LightSteelBlue}{ {{(state.lambda_obs/state.lambda_rest-1).toFixed(5)}} } } $$
              <p>
                Great work. Here is your galaxy's velocity:
              </p>
              <v-card color="info" class="pa-3">
                $$ v = \textcolor{black}{\colorbox{LightSteelBlue}{ {{ state.student_vel.toFixed(0).toLocaleString() }} } }   \text{ km/s}$$
              </v-card>
              <v-divider role="presentation"></v-divider>
              <p class="pt-5 font-weight-light">
                \(v\): velocity of your galaxy, in km/s <br>
                \(c\): speed of light, 300,000 km/s <br>
                \(\lambda_{\text{obs}}\): observed wavelength of spectral line in your galaxy <br>
                \(\lambda_{\text{rest}}\): rest wavelength of spectral line} <br>
              </p>
            </v-card-text>
          </v-window-item>

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
                :disabled="n > maxStepCompleted5 + 2"
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
            v-if="step <4"
            :disabled="step > maxStepCompleted5"
            color="accent"
            text
            @click="step++;"
          >
            {{ (step < 2 ) ? 'calculate' : 'next' }}
          </v-btn>
          <v-btn
            v-if="step == 4"
            class="black--text"
            color="accent"
            elevation="2"
            @click="() => {
              const lambdas = [state.lambda_obs, state.lambda_rest];
              validateLightSpeed(['speed_light']) ? step++ : null;
              storeStudentc(['speed_light']);
              state.student_vel = storeStudentVel(studentc, lambdas);
            }"
          >
           {{ (!failedValidation5 ) ? 'next' : 'try again' }}
          </v-btn>
          <v-btn
            v-if="step==5"
            color="accent"
            class="black--text"
            depressed
            @click="() => { 
              $emit('submit'); 
              state.doppler_calc_dialog = false; 
              step = 0; 
              state.marker='dop_cal6'; 
              state.dopper_calc_complete = true}"
          >
            Done
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

</template>


<script>
export default = {
  methods: {
    getValue(inputID) {
      const input = document.getElementById(inputID);
      if (!input) { return null; }
      return input.value;
    },

    parseAnswer(inputID) {
      return parseFloat(this.getValue(inputID).replace(/,/g,''));
    },

    storeStudentc(inputID) {
      return this.studentc = this.parseAnswer(inputID);
    },

    storeStudentVel(studentc, lambdas) {
      return studentc * (lambdas[0]/lambdas[1] - 1);
    },

    validateLightSpeed(inputIDs) {
      return inputIDs.every((id, index) => {
        const value = this.parseAnswer(id);
        this.failedValidation5 = ( value <= 3e5 && value >= 299790 ) ? false : true;
        return value <= 3e5 && value >= 299790;
      });
    }
  },
  watch: {
    step(newStep, oldStep) {
        const isInteractStep = this.interactSteps5.includes(newStep);
        const newCompleted = isInteractStep ? newStep - 1 : newStep;
        this.maxStepCompleted5 = Math.max(this.maxStepCompleted5, newCompleted)
    }
  }
};
</script>