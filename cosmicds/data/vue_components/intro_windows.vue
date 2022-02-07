<template>
  <v-card>
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
    </v-card-title>

    <v-window
      style="min-height: 250px;"
      v-model="step"
    >
      <v-window-item :value="0" 
        class="no-transition"
      >
        <v-card-text>
          <p>
            Welcome to this Cosmic Data Story. In this activity, you will use real astronomical data to answer big questions about our universe, such as:
          </p>
          <ul>
            <li>Has the universe always existed? If not, how long ago did it form?</li>
          </ul>
          <p>
            While answering these big questions, you will learn techniques scientists use to assess how reliable they think a result is, based on their data. After all, when scientists collect data to answer new questions, there is no answer key that they can use to check their answers. They have to determine for themselves what conclusions can be drawn from their data.
          </p>
          <p>
            You will do the same thing in this Data Story. Let’s get started!
          </p>
        </v-card-text>
      </v-window-item>


      <v-window-item :value="1" 
        class="no-transition"
      >
        <v-card-text>
          <p>
            Imagine that you are an astronomer living a century ago in the early 1920's. Pretty much all scientists of this time, including Albert Einstein, believed that the universe was static, unchanging, and eternal (meaning that the universe has always been and always will be). These ideas date back to ancient Greek times and were embraced by philosophers such as Aristotle.
          </p>
          <ul>
            <li>Pictures of old telescopes &amp; astronomers</li>
          </ul>
        </v-card-text>
      </v-window-item>

      <v-window-item :value="2" 
        class="no-transition"
      >
        <v-card-text>
          <p>
            This window provides a view of the "night sky." You can explore this view and see what is in the night sky, as astronomers have been doing for centuries.
          </p>
          <div
            class="mb-2 mx-4"
          >
            <v-row
              no-gutters
              class="mb-3"
            >
              <v-col
                cols="3"
              >
                <strong>Pan</strong>
              </v-col>
              <v-col
                cols="9"
              >
                <strong>click + drag</strong><br>
                (or use the <strong class="codeFont">I-J-K-L</strong> keys)
              </v-col>
            </v-row>
            <v-row
              no-gutters
            >
              <v-col
                cols="3"
              >
                <strong>Zoom</strong>
              </v-col>
              <v-col
                cols="9"
              >
                <strong>scroll in and out</strong><br>
                (or use the <strong class="codeFont">Z-X</strong> keys for finer zoom)
              </v-col>
            </v-row>
          </div>
        </v-card-text>
      </v-window-item>

      <v-window-item :value="3" 
        class="no-transition"
      >
        <v-card-text>
          <p>
            As you pan through the sky, you may see stars and fuzzy blobs called nebulae. Astronomers in the early 1900’s wondered whether these nebulae are contained within our Milky Way galaxy or located beyond it.
          </p>
          <p>
            Click on the thumbnails to go directly to some different nebulae catalogued by French astronomer Charles Messier in the 1700’s:
          </p>
        </v-card-text>
      </v-window-item>

      <v-window-item :value="4" 
        class="no-transition"
      >
        <v-card-text>
          <p>
            One particular type of nebulae, known as “spiral” nebulae because of their distinctive spiral shape, became of particular interest in the early 1900’s. In 1920, there was a “Great Debate” between astronomers Harlow Shapley &amp; Heber Curtis questioning whether the spiral nebulae were part of our own Milky Way galaxy or were “island universes” beyond our Milky Way. Do you think these nebulae you’ve observed are within the Milky Way or beyond it?
          </p>
        </v-card-text>
      </v-window-item>

      <v-window-item :value="5" 
        class="no-transition"
      >
        <v-card-text>
          <p>
            Around this same time, astronomer Vesto Slipher was observing these spiral nebulae using a spectrograph. A spectrograph separates the light from a source into its distinct colors, as a prism does. By measuring the brightness of the light in each color (or wavelength), you can learn a lot about an object in space, like what it is made of or how fast it is moving toward or away from you.
          </p>
          <p>
            Recall that the prevailing view in the early 1900’s was that that the universe is unchanging and eternal, so the expectation was that the nebulae are either not moving at all, or perhaps they are moving randomly.
          </p>
          <p>
            what Slipher found.
          </p>
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
        :disabled="step === 5"
        color="accent"
        text
        @click="step++;"
      >
        {{ step < 5 ? 'next' : '' }}
      </v-btn>
      <v-btn
        :disabled="step > 5"
        color="accent"
        class="black--text"
        depressed
        @click="() => { $emit('continue'); step = 0; }"
      >
        {{ continueText }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>


<style>

.no-transition {
  transition: none;
}

</style>


<script>
module.exports = {
  props: ["continueText"],
  data: function () {
    return {
      step: 0,
      length: 6,
      dialog: false
    };
  },
  computed: {
    currentTitle () {
      switch (this.step) {
        case 0: return 'Intro 1'
        case 1: return 'Intro 2'
        case 2: return 'Intro 3'
        case 3: return 'Intro 4'
        case 4: return 'Intro 5'
        default: return 'Intro 6'
      }
    },
  },
};
</script>

<style>

div {
  color: "purple";
}

</style>