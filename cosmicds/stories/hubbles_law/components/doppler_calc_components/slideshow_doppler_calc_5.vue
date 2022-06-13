<template>
  <v-dialog
      v-model="state.doppler_calc_dialog"
      persistent
      max-width="800px"
  >
    <v-card
      class="mx-auto"
    >
      <v-toolbar
        color="info darken-1"
        dense
        dark
      >
        <v-toolbar-title
          class="text-h6 text-uppercase font-weight-regular"
        >
          {{ currentTitle }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
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
      </v-toolbar>

      <v-window
        v-model="step"
        vertical
        style="height: 70vh;"
        class="overflow-auto"
      >

        <v-window-item :value="0"
          class="no-transition"
        >
          <v-card-text
            class="pt-8"
            v-intersect="(entries, _observer, intersecting) => {
              if (!intersecting) return;
              const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
              MathJax.typesetPromise(targets);
            }"
          >
            <p>
              Great! Now we'll continue the velocity calculation process in the sequence of this pop-up window to give ourselves some more space to work.
            </p>
            <p>
              You can click the header and drag if you want to move the pop-up around to see content behind it.
            </p>
            <v-card
              color="info"
              class="JaxEquation pa-3"
            >
              $$ v = c \times \left( \frac{\textcolor{black}{\colorbox{#FFAB91}{ {{ state.lambda_obs }} }} \text{ &#8491;}}{\textcolor{black}{\colorbox{#FFAB91}{ {{ state.lambda_rest }} }} \text{ &#8491;}} - 1 \right) $$
              <v-divider role="presentation"></v-divider>
              <div
                class="font-weight-medium mt-3"
              >
                Click <strong>CALCULATE</strong> to compute the value of the fraction you entered.
              </div>
            </v-card>
            <v-divider role="presentation"></v-divider>
            <v-card
              class="legend mt-8"
            >
              <v-container>
                <v-row
                  no-gutters
                >
                  <v-col>
                    <div
                      class="JaxEquation"
                    >
                      $$ v = c \times \left( \frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}} - 1 \right) $$
                    </div>
                  </v-col>
                </v-row>
                <v-divider></v-divider>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    
                  >
                    \(v\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    velocity of your galaxy, in km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(c\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    speed of light, 300,000 km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(\lambda_{\text{obs}}\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    observed wavelength of spectral line in your galaxy
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(\lambda_{\text{rest}}\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    rest wavelength of spectral line
                  </v-col>
                </v-row>
              </v-container>
            </v-card>
          </v-card-text>
        </v-window-item>


        <v-window-item :value="1"
          class="no-transition"
        >
          <v-card-text
            class="pt-8"
            v-intersect="(entries, _observer, intersecting) => {
              if (!intersecting) return;
              const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
              MathJax.typesetPromise(targets);
            }"
          >
            <v-card
              class="JaxEquation past_block pa-3"
            >
              $$ v = c \times \left( \frac{\textcolor{black}{\colorbox{#9E9E9E}{ {{ state.lambda_obs }} }} \text{ &#8491;}}{\textcolor{black}{\colorbox{#9E9E9E}{ {{ state.lambda_rest }} }} \text{ &#8491;}} - 1 \right) $$
            </v-card>
            <p>
              Dividing the fraction gives you <strong>{{ (state.lambda_obs/state.lambda_rest).toFixed(4) }}</strong>. Now we have:
            </p>
            <v-card
              color="info"
              class="JaxEquation pa-3"
            >
              $$ v = c \times \left( \textcolor{black}{\colorbox{#FFAB91}{ {{ (state.lambda_obs/state.lambda_rest).toFixed(4) }} } } - 1 \right) $$
              <v-divider role="presentation"></v-divider>
              <div
                class="font-weight-medium mt-3"
              >
                Click <strong>CALCULATE</strong> to perform the subtraction.
              </div>
            </v-card>
            <v-divider role="presentation"></v-divider>
            <v-card
              class="legend mt-8"
            >
              <v-container>
                <v-row
                  no-gutters
                >
                  <v-col>
                    <div
                      class="JaxEquation"
                    >
                      $$ v = c \times \left( \frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}} - 1 \right) $$
                    </div>
                  </v-col>
                </v-row>
                <v-divider></v-divider>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    
                  >
                    \(v\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    velocity of your galaxy, in km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(c\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    speed of light, 300,000 km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(\lambda_{\text{obs}}\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    observed wavelength of spectral line in your galaxy
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(\lambda_{\text{rest}}\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    rest wavelength of spectral line
                  </v-col>
                </v-row>
              </v-container>
            </v-card>
          </v-card-text>
        </v-window-item>


        <v-window-item :value="2"
          class="no-transition"
        >
          <v-card-text
            class="pt-8"
            v-intersect="(entries, _observer, intersecting) => {
              if (!intersecting) return;
              const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
              MathJax.typesetPromise(targets);
            }"
          >
            <v-card
              class="JaxEquation past_block pa-3"
            >
              $$ v = c \times \left( \frac{\textcolor{black}{\colorbox{#9E9E9E}{ {{ state.lambda_obs }} }} \text{ &#8491;}}{\textcolor{black}{\colorbox{#9E9E9E}{ {{ state.lambda_rest }} }} \text{ &#8491;}} - 1 \right) $$ 

              $$ v = c \times \left( \textcolor{black}{\colorbox{#9E9E9E}{ {{(state.lambda_obs/state.lambda_rest).toFixed(4)}} } } - 1 \right) $$
            </v-card>
            <p>
              Subtracting 1 gives you <strong>{{(state.lambda_obs/state.lambda_rest-1).toFixed(4)}}</strong>. Now we are left with:
            </p>
            <v-card
              color="info"
              class="JaxEquation pa-3"
            >
              $$ v = c \times \textcolor{black}{\colorbox{#FFAB91}{ {{(state.lambda_obs/state.lambda_rest-1).toFixed(4)}} } } $$
              <v-divider role="presentation"></v-divider>
              <div
                class="font-weight-medium mt-3"
              >
                Click <strong>NEXT</strong> to continue.
              </div>
            </v-card>
            <v-divider role="presentation"></v-divider>
            <v-card
              class="legend mt-8"
              outlined
            >
              <v-container>
                <v-row
                  no-gutters
                >
                  <v-col>
                    <div
                      class="JaxEquation"
                    >
                      $$ v = c \times \left( \frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}} - 1 \right) $$
                    </div>
                  </v-col>
                </v-row>
                <v-divider></v-divider>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    
                  >
                    \(v\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    velocity of your galaxy, in km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(c\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    speed of light, 300,000 km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(\lambda_{\text{obs}}\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    observed wavelength of spectral line in your galaxy
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(\lambda_{\text{rest}}\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    rest wavelength of spectral line
                  </v-col>
                </v-row>
              </v-container>
            </v-card>
          </v-card-text>
        </v-window-item>


        <v-window-item :value="3"
          class="no-transition"
        >
          <v-card-text
            class="pt-8"
            v-intersect="(entries, _observer, intersecting) => {
              if (!intersecting) return;
              const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
              MathJax.typesetPromise(targets);
            }"
          >
            <v-card
              color="info"
              class="JaxEquation pa-3"
            >
              $$ v = c \times \textcolor{black}{\colorbox{#FFAB91}{ {{(state.lambda_obs/state.lambda_rest-1).toFixed(4)}} } } $$
            </v-card>
            <v-container>
              <v-row>
                <v-col>
                  <p class="mb-0">
                    Reflect for a bit on what this means. How does the velocity of your galaxy relate to the speed of light?
                  </p>
                  <mc-radiogroup
                    :radio-options="[
                      'There is no relationship between my galaxy\’s velocity and the speed of light.',
                      'My galaxy\’s velocity is a fraction of the speed of light. ',
                      'My galaxy\’s velocity is greater than the speed of light.'
                    ]"
                    :feedbacks="[
                      'Try again. The equation describes a relationship between your galaxy\’s velocity and the speed of light.',
                      'Correct. The fraction is the ratio of the observed wavelength of my spectral line over the line’s rest wavelength minus 1. This will be the case for all of your galaxies.',
                      'Try again. You are multiplying the speed of light by a value that is smaller than 1.'
                    ]"
                    :correct-answers="[1]"
                    :selected-callback="(state) => { if(state.correct) { this.maxStepCompleted5 = Math.max(this.maxStepCompleted5, 3); } }"  
                  >
                  </mc-radiogroup>
                </v-col>
              </v-row>
            </v-container>
            <v-divider role="presentation"></v-divider>
            <v-card
              class="legend mt-8"
            >
              <v-container>
                <v-row
                  no-gutters
                >
                  <v-col>
                    <div
                      class="JaxEquation"
                    >
                      $$ v = c \times \left( \frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}} - 1 \right) $$
                    </div>
                  </v-col>
                </v-row>
                <v-divider></v-divider>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    
                  >
                    \(v\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    velocity of your galaxy, in km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(c\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    speed of light, 300,000 km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(\lambda_{\text{obs}}\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    observed wavelength of spectral line in your galaxy
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(\lambda_{\text{rest}}\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    rest wavelength of spectral line
                  </v-col>
                </v-row>
              </v-container>
            </v-card>
          </v-card-text>
        </v-window-item>


        <v-window-item :value="4"
          class="no-transition"
        >
          <v-card-text
            class="pt-8"
            v-intersect="(entries, _observer, intersecting) => {
              if (!intersecting) return;
              const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
              MathJax.typesetPromise(targets);
            }"
          >
            <p>
              Now enter the <strong>speed of light</strong> in <strong>km/s</strong> in the empty box below.
            </p>
            <v-card
              color="info"
              class="JaxEquation pa-3"
            >
              $$ v = c \times \textcolor{black}{\colorbox{#FFAB91}{ {{(state.lambda_obs/state.lambda_rest-1).toFixed(4)}} } } $$
              $$ v = \bbox[#FBE9E7]{\input[speed_light][]{}} \text{ km/s} \times \textcolor{black}{\colorbox{#FFAB91}{ {{(state.lambda_obs/state.lambda_rest-1).toFixed(4)}} } } $$
              <v-divider role="presentation"></v-divider>
              <div
                class="font-weight-medium mt-3"
              >
                Click <strong>CALCULATE</strong> to multiply through and obtain the speed of your galaxy.
              </div>
              <v-alert
                v-if="failedValidation5"
                dense
                color="info darken-1"
                style="font-size: 16px;"
                class="my-3"
              >
                Try again. Check that you are using <strong>km/s</strong>, and make sure you have the correct number of zeroes. The speed of light is highlighted in yellow below.
              </v-alert>
            </v-card>
            <v-divider role="presentation"></v-divider>
            <v-card
              class="legend mt-8"
            >
              <v-container>
                <v-row
                  no-gutters
                >
                  <v-col>
                    <div
                      class="JaxEquation"
                    >
                      $$ v = c \times \left( \frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}} - 1 \right) $$
                    </div>
                  </v-col>
                </v-row>
                <v-divider></v-divider>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    
                  >
                    \(v\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    velocity of your galaxy, in km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                  v-if="!failedValidation5"
                >
                  <v-col
                    cols="2"
                  >
                    \(c\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    speed of light, 300,000 km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1 yellow--text font-weight-medium"
                  v-if="failedValidation5"
                  v-intersect="(entries, _observer, intersecting) => {
                    if (!intersecting) return;
                    const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
                    MathJax.typesetPromise(targets);
                  }"
                >
                  <v-col
                    cols="2"
                  >
                    \(c\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    speed of light, 300,000 km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(\lambda_{\text{obs}}\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    observed wavelength of spectral line in your galaxy
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(\lambda_{\text{rest}}\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    rest wavelength of spectral line
                  </v-col>
                </v-row>
              </v-container>
            </v-card>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="5"
          class="no-transition"
        >
          <v-card-text
            class="pt-8"
            v-intersect="(entries, _observer, intersecting) => {
              if (!intersecting) return;
              const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
              MathJax.typesetPromise(targets);
            }"
          >
            <v-card
              class="JaxEquation past_block pa-3"
            >
              $$ v = c \times \left( \frac{\textcolor{black}{\colorbox{#9E9E9E}{ {{ state.lambda_obs }} }} \text{ &#8491;}}{\textcolor{black}{\colorbox{#9E9E9E}{ {{ state.lambda_rest }} }} \text{ &#8491;}} - 1 \right) $$ 

              $$ v = c \times \left( \textcolor{black}{\colorbox{#9E9E9E}{ {{(state.lambda_obs/state.lambda_rest).toFixed(4)}} } } - 1 \right) $$

              $$ v = c \times \textcolor{black}{\colorbox{#9E9E9E}{ {{(state.lambda_obs/state.lambda_rest-1).toFixed(4)}} } } $$

              $$ v = \textcolor{black}{\colorbox{#9E9E9E}{ {{ studentc.toLocaleString() }} } } \text{ km/s} \times \textcolor{black}{\colorbox{#9E9E9E}{ {{(state.lambda_obs/state.lambda_rest-1).toFixed(4)}} } } $$
            </v-card>
            <p>
              Great work. Your galaxy's velocity is <strong>{{ state.student_vel.toFixed(0).toLocaleString() }}</strong> km/s.
            </p>
            <v-card
              color="info"
              class="JaxEquation pa-3"
            >
              $$ v = \textcolor{black}{\colorbox{#FFAB91}{ {{ state.student_vel.toFixed(0).toLocaleString() }} } } \text{ km/s} $$
              <v-divider role="presentation"></v-divider>
              <div
                class="font-weight-medium mt-3"
              >
                Click <strong>DONE</strong> to close this pop-up window. Your velocity will fill into your table for this galaxy.
              </div>
            </v-card>
            <v-divider role="presentation"></v-divider>
            <v-card
              class="legend mt-8"
            >
              <v-container>
                <v-row
                  no-gutters
                >
                  <v-col>
                    <div
                      class="JaxEquation"
                    >
                      $$ v = c \times \left( \frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}} - 1 \right) $$
                    </div>
                  </v-col>
                </v-row>
                <v-divider></v-divider>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    
                  >
                    \(v\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    velocity of your galaxy, in km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(c\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    speed of light, 300,000 km/s
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(\lambda_{\text{obs}}\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    observed wavelength of spectral line in your galaxy
                  </v-col>
                </v-row>
                <v-row
                  no-gutters
                  class="my-1"
                >
                  <v-col
                    cols="2"
                  >
                    \(\lambda_{\text{rest}}\)
                  </v-col>
                  <v-col
                    cols="10"
                  >
                    rest wavelength of spectral line
                  </v-col>
                </v-row>
              </v-container>
            </v-card>
          </v-card-text>
        </v-window-item>
      </v-window>

      <v-divider></v-divider>

      <v-card-actions>
        <v-btn
          :disabled="step === 0"
          color="accent"
          class="black--text"
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
          v-if="step < 4"
          :disabled="step > maxStepCompleted5"
          class="black--text"
          color="accent"
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
          calculate
        </v-btn>
        <v-btn
          v-if="step==5"
          color="accent"
          class="black--text"
          v-model="student_vel_calc"
          depressed
          @click="() => { 
            $emit('submit'); 
            state.doppler_calc_dialog = false; 
            step = 0; 
            state.marker='dop_cal6'; 
            state.doppler_calc_complete = true;
            console.log('calc done:', state.doppler_calc_complete);
            student_vel_calc = true}"
        >
          Done
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>


<style>

.JaxEquation .MathJax {
  margin: 20px auto !important;
}

mjx-mpadded {
  border-radius: 5px;
}

.v-application .past_block {
  border: 1px solid #FF5722 !important;
  margin-bottom: 16px;
}

.v-application .past_block mjx-math {
  font-size: 16px !important;
}

.v-application .legend {
  max-width: 300px;
  margin: 0 auto 0;
  font-size: 15px !important;
}

#speed_light {
  color:  black;
  font-size: 18px;
  font-family: "Roboto", Arial, Helvetica, sans-serif;
  padding: 3px;
}

</style>


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
