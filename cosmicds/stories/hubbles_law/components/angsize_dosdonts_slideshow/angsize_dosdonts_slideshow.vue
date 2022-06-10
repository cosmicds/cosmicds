<template>
  <v-btn
    class="my-2"
    block
    color="secondary"
    elevation="2"
    @click.stop="dialog = true"
  >
    dos and donts

    <v-dialog
        v-model="dialog"
        persistent
        max-width="1000px"
    >
      <v-card
        class="mx-auto"
      >
        <v-toolbar
          color="secondary"
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
            @click="
              () => {
                $emit('close');
                dialog = false;
                if (step == 8) {
                  step = 0;
                }
              }
            "
          >
            <v-btn icon>
              <v-icon> mdi-close </v-icon>
            </v-btn>
          </span>
        </v-toolbar>

          <v-window
            v-model="step"
            style="height: 70vh;"
            class="overflow-auto"
          >

          <v-window-item :value="0" class="no-transition">
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col>
                    <h3 class="mb-4">Header</h3>
                    <p>
                      lorem ispum dolor sit amet
                    </p>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col
                    cols="6"
                    class="d-flex flex-column"
                    height="100%"
                    flat
                    tile
                  >
                    <h4>Caption Header</h4>
                    <p>
                      Caption
                    </p>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${state.image_location_dosdonts}/Bright-Spiral-DO.png`"
                    ></v-img>
                  </v-col>
                  <v-col cols="6">
                    <h4>Caption Header</h4>
                    <p>
                      Caption
                    </p>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${state.image_location_dosdonts}/Bright-Spiral-DONT.png`"
                    ></v-img>
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
                    <h3 class="mb-4">Header</h3>
                    <p>
                      lorem ispum dolor sit amet
                    </p>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col
                    cols="4"
                    class="d-flex flex-column"
                    height="100%"
                    flat
                    tile
                  >
                    <h4>Caption Header</h4>
                    <p>
                      Caption
                    </p>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${state.image_location_dosdonts}/Bright-Spiral-DO.png`"
                    ></v-img>
                  </v-col>
                  <v-col cols="4">
                    <h4>Caption Header</h4>
                    <p>
                      Caption
                    </p>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${state.image_location_dosdonts}/Bright-Spiral-DONT.png`"
                    ></v-img>
                  </v-col>
                  <v-col cols="4">
                    <h4>Caption Header</h4>
                    <p>
                      Caption
                    </p>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${state.image_location_dosdonts}/Bright-Spiral-DONT.png`"
                    ></v-img>
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
            v-if="step < length-1"
            color="accent"
            text
            @click="step++;"
          >
            {{ step < length-1 ? 'next' : '' }}
          </v-btn>
          <v-btn
            v-if = "step == length-1"
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

<script>
module.exports = {
  props: ["buttonText", "titleText", "closeText"],

  watch: {
    step(newStep, oldStep) {
      const isInteractStep = this.interact_steps.includes(newStep);
      console.log("Interact Step", this.interact_steps);
      const newCompleted = isInteractStep ? newStep - 1 : newStep;
      this.max_step_completed = Math.max(this.max_step_completed, newCompleted);
    },
  },
};
</script>

<style>
.no-transition {
  transition: none;
}
</style>
