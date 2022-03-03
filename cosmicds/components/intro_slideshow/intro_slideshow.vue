<template>
  <v-card
    class="darken"
  >
    <v-card-title
      class="text-h6 font-weight-regular justify-space-between;"
    >
      <span>
        <!--
        <v-avatar
          color="info"
          class="subheading white--text mr-4"
          size="24"
          v-text="step"
        ></v-avatar>
        -->
        {{ currentTitle }}
      </span>
    </v-card-title>

    <v-window
      style="min-height: 300px;"
      v-model="step"
    >
      <v-window-item :value="0" 
        class="no-transition"
      >
        <v-card-text>
          <p>
            Welcome to the Cosmic Data Story about the Hubble Law. In this activity, you will use real astronomical data to answer these questions about our universe:
          </p>
          <p 
            style="text-align:center; font-weight:600;"
          >
            Has the universe always existed? If not, how long ago did it form?
          </p>
          <p>
            While answering these questions, you will learn techniques scientists use to assess how reliable they think a result is, based on their data. After all, when scientists collect data to answer new questions, there is no answer key that they can use to check their answers. They have to determine for themselves what conclusions can be drawn from their data.
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
          <p
            style="text-align:center;"
          >
            (Pictures of old telescopes &amp; astronomers)
          </p>
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
            <v-row>
              <v-col
                cols="8"
              >
                <v-card
                  outlined
                  color="info"
                  class="pa-1"
                >
                  <v-toolbar
                    color="secondary"
                    dense
                    dark
                  >
                    <v-toolbar-title>Night Sky Viewer</v-toolbar-title>
                    <!--<v-tooltip top>-->
                      <div class="text-center">
                        <v-dialog
                          v-model="dialog"
                          width="600"
                        >
                          <template v-slot:activator="{ on, attrs }">
                              <v-btn 
                                icon
                                right
                                v-bind="attrs"
                                v-on="on"
                              >
                                <v-icon>mdi-information-outline</v-icon>
                              </v-btn>
                          </template>
                          <v-card>
                            <v-card-title>
                              Data Tool and Imagery credits
                            </v-card-title>
                            <v-card-text>
                              lorem ipsum
                            </v-card-text>
                            <v-card-actions>
                              <v-spacer></v-spacer>
                              <v-btn
                                text
                                @click="dialog = false"
                              >
                              Close
                              </v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-dialog>
                      </div>
                      <!--
                      Data tool and imagery credits
                    </v-tooltip>-->
                    <v-spacer></v-spacer>   
                  </v-toolbar>         
                    <c-exploration-tool>
                </v-card>
              </v-col>
              <v-col
                cols="4"
              >
                <v-row>
                  <v-col
                    cols="4"
                  >
                    <strong>Pan</strong>
                  </v-col>
                  <v-col
                    cols="8"
                  >
                    <strong>click + drag</strong><br>
                    (or use the <strong class="codeFont">I-J-K-L</strong> keys)
                  </v-col>
                </v-row>
                <v-row>
                  <v-col
                    cols="4"
                  >
                     <strong>Zoom</strong>
                  </v-col>
                  <v-col
                    cols="8"
                  >
                    <strong>scroll in and out</strong><br>
                    (or use the <strong class="codeFont">Z-X</strong> keys for finer zoom)
                  </v-col>
                </v-row>
              </v-col>
            </div>                                        
            

<!--
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
                cols="3"
              >
                <strong>click + drag</strong><br>
                (or use the <strong class="codeFont">I-J-K-L</strong> keys)
              </v-col>
              <v-col
                cols="3"
              >
                <strong>Zoom</strong>
              </v-col>
              <v-col
                cols="3"
              >
                <strong>scroll in and out</strong><br>
                (or use the <strong class="codeFont">Z-X</strong> keys for finer zoom)
              </v-col>
              <v-col
                cols="6"
              >
              <v-btn
                @click="go_to_location({
                    ra: 83.63,
                    dec: 22.01,
                    fov: 350, // optional, in arcseconds, default is 90
                    instant: false // also optional, false by default
                  })"
              >
                Example Messier button (M1)
              </v-btn>
              <c-exploration-tool id="exploration-tool">
              </v-col>
            </v-row>

-->
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
            M31 is an example of a particular type of nebula that interested astronomers in the early 1900’s. They were known as “spiral” nebulae because of their distinctive spiral shape. In 1920, there was a “Great Debate” between astronomers Harlow Shapley and Heber Curtis questioning whether the spiral nebulae were part of our own Milky Way galaxy or were “island universes” beyond our Milky Way. Do you think the nebulae you’ve observed are within the Milky Way or beyond it?
          </p>
        </v-card-text>
      </v-window-item>

      <v-window-item :value="5" 
        class="no-transition"
      >
        <v-card-text>
          <p>
            Between 1907&#8211;1921, astronomer Henrietta Leavitt discovered and observed Cepheid variable stars. She noticed an important property about these stars, that there is a relationship between the intrinsic brightness of the Cepheids and how slowly or rapidly their brightness changes. This important discovery made it possible to determine distances to the nebulae and finally resolve the Shapley-Curtis Great Debate&#8212;many of the nebulae are far beyond the Milky Way and constitute individual galaxies in their own right.
          </p>
          <p
            style="text-align:center;"
          >
            (Pictures of Henrietta's glass plates)
          </p>
        </v-card-text>
      </v-window-item>

      <v-window-item :value="6" 
        class="no-transition"
      >
        <v-card-text>
          <p>
            Around this same time, astronomer Vesto Slipher observed galaxies using a spectrograph. Spectrographs can tell you a lot about an object in space, like what it is made of or how fast it is moving toward or away from you. 
          </p>
          <p>
            Recall that the prevailing view in the early 1900’s was that that the universe is unchanging and eternal, so the expectation was that the galaxies are either not moving at all, or perhaps they are moving randomly. 
          </p>
          <p>
            It’s time for you to collect some of your own data to learn what Slipher found.
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
        :disabled="step === 6 || (step === 2 && !exploration_complete)"
        color="accent"
        text
        @click="step++;"
      >
        {{ step < 6 ? 'next' : '' }}
      </v-btn>
      <v-btn
        :disabled="step > 6"
        color="accent"
        class="black--text"
        depressed
        @click="() => { 
          $emit('continue');
          step = 0;
        }"
      >
        get started
      </v-btn>
    </v-card-actions>
  </v-card>
</template>


<style>
.no-transition {
  transition: none;
}
.darken {
  background-image: 
    linear-gradient(
      rgba(0, 0, 0, 0.7),
      rgba(0, 0, 0, 0.7)
    ),
    /* url(https://astropix.ipac.caltech.edu/archive/noirlab/stsci-gallery-1427a-2000x960/noirlab_stsci-gallery-1427a-2000x960_1600.jpg); */
}
.v-card__text{
  padding: 0px 15px 0px;
}

#exploration-tool {
  height: 300px;
}
</style>


<script>
module.exports = {
  props: ["continueText"],
};
</script>

<style>

div {
  color: "purple";
}

</style>
