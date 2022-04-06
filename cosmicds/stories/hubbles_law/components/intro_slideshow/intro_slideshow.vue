<template>
  <v-card
    id="slideshow-root"
    outlined
    elevation="6"
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
    </v-toolbar>

    <v-window
      style="min-height: 300px;"
      v-model="step"
    >
      <v-window-item :value="0" 
        class="no-transition"
      >
        <v-card-text
          style="min-height: 550px;"
        >
          <v-container>
            <v-row
              no-gutter
            >
              <v-col cols="7">
                <p>
                  Welcome to the Cosmic Data Story about the Hubble Law. In this activity, you will use real astronomical data to answer these questions about our universe:
                </p>
                <v-card
                  class="d-flex justify-center pa-4 mx-12 mb-4"
                  color="secondary"
                  style="font-weight:600;"
                >
                  Has the universe always existed? If not, how long ago did it form?
                </v-card>
                <p>
                  While answering these questions, you will learn techniques scientists use to assess how reliable they think a result is, based on their data. After all, when scientists collect data to answer new questions, there is no answer key that they can use to check their answers. They have to determine for themselves what conclusions can be drawn from their data.
                </p>
                <p>
                  You will do the same thing in this Data Story. Let’s get started!
                </p>
              </v-col>
              <v-col cols="5">
                <v-img
                  lazy-src="https://astropix.ipac.caltech.edu/archive/esahubble/heic0406a/esahubble_heic0406a_320.jpg"
                  src="https://astropix.ipac.caltech.edu/archive/esahubble/heic0406a/esahubble_heic0406a_320.jpg"
                  alt="Image of distant galaxies taken by the Hubble Space Telescope"
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
          <div
            style="min-height: 100px;"
          >
            <p>
              This window provides a view of the "night sky," based on actual telescopic data. You can explore this view, as astronomers have been doing for centuries.
            </p>
          </div>
          <div
            class="mb-2 mx-4"
          >    
            <v-row>
              <v-col
                cols="8"
                offset-lg="1"
              >   
                <c-exploration-tool id="exploration-tool">
              </v-col>
              <v-col
                cols="4"
                lg="3"
              >
                <v-row>
                  <v-col
                    cols="12"
                    lg="4"
                  >
                    <v-chip
                      label
                      outlined
                    >
                      Pan
                    </v-chip>
                  </v-col>
                  <v-col
                    cols="12"
                    lg="8"
                    class="pt-2"
                  >
                    <strong>click + drag</strong><br>
                    (or use <strong class="codeFont">I-J-K-L</strong> keys)
                  </v-col>
                </v-row>
                <v-row>
                  <v-col
                    cols="12"
                    lg="4"
                  >
                    <v-chip
                      label
                      outlined
                    >
                      Zoom
                    </v-chip>
                  </v-col>
                  <v-col
                    cols="12"
                    lg="8"
                    class="pt-2"
                  >
                    <strong>scroll in and out</strong><br>
                    (or use <strong class="codeFont">Z-X</strong> keys)
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </div>                                        
        </v-card-text>
       </v-window-item>

      <v-window-item :value="3" 
        class="no-transition"
      >
        <v-card-text>
          <div
            style="min-height: 100px;"
          >
            <p>
              As you pan through the sky, you may see stars and fuzzy blobs called nebulae. In the 1700's, French astronomer Charles Messier cataloged as many nebulae as he could find. They are known as "Messier Objects" and are identified by their catalog number.
            </p>
            <p>
              Click on the thumbnails to view some Messier Objects:
            </p>
          </div>
          <div
            class="mb-2 mx-4"
          >    
            <v-row>
              <v-col
                cols="8"
                offset-lg="1"
              >   
                <c-exploration-tool2 id="exploration-tool2">
              </v-col>
              <v-col
                cols="4"
                lg="2"
              >
                <v-row
                  justify="space-between"
                >
                  <v-col
                    cols="12"
                    lg="6"
                  >
                    <v-btn
                      @click="go_to_location_tool2({
                          ra: 83.63,
                          dec: 22.014,
                          fov: 350, // optional, in arcseconds, default is 90
                          instant: false // also optional, false by default
                        })"
                      color="info"
                      width="100%"
                      class="mx-2"
                    >
                      M1
                    </v-btn>
                  </v-col>
                  <v-col
                    cols="12"
                    lg="6"
                  >
                    <v-btn
                      @click="go_to_location_tool2({
                          ra: 250.4,
                          dec: 36.46,
                          fov: 700, // optional, in arcseconds, default is 90
                          instant: false // also optional, false by default
                        })"
                      color="info"
                      width="100%"
                      class="mx-2"
                    >
                      M13
                    </v-btn>
                  </v-col>
                  <v-col
                    cols="12"
                    lg="6"
                  >
                    <v-btn
                      @click="go_to_location_tool2({
                          ra: 10.63,
                          dec: 41.27,
                          fov: 6000, // optional, in arcseconds, default is 90
                          instant: false // also optional, false by default
                        })"
                      color="info"
                      width="100%"
                      class="mx-2"
                    >
                      M31
                    </v-btn>
                  </v-col>
                  <v-col
                    cols="12"
                    lg="6"
                  >
                    <v-btn
                      @click="go_to_location_tool2({
                          ra: 83.82,
                          dec: -5.39,
                          fov:7500, // optional, in arcseconds, default is 90
                          instant: false // also optional, false by default
                        })"
                      color="info"
                      width="100%"
                      class="mx-2"
                    >
                      M42
                    </v-btn>
                  </v-col>
                  <v-col
                    cols="12"
                    lg="6"
                  >
                    <v-btn
                      @click="go_to_location_tool2({
                          ra: 202.47,
                          dec: 47.195,
                          fov: 700, // optional, in arcseconds, default is 90
                          instant: false // also optional, false by default
                        })"
                      color="info"
                      width="100%"
                      class="mx-2"
                    >
                      M51
                    </v-btn>
                  </v-col>
                  <v-col
                    cols="12"
                    lg="6"
                  >
                    <v-btn
                      @click="go_to_location_tool2({
                          ra: 148.97,
                          dec: 69.68,
                          fov: 400, // optional, in arcseconds, default is 90
                          instant: false // also optional, false by default
                        })"
                      color="info"
                      width="100%"
                      class="mx-2"
                    >
                      M82
                    </v-btn>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </div>         
        </v-card-text>
      </v-window-item>

      <v-window-item :value="4" 
        class="no-transition"
      >
        <v-card-text>
          <div
            style="min-height: 100px;"
          >
            <p>
              M31 and M51 are examples of a particular type of nebula that interested astronomers in the early 1900’s. They were known as “spiral” nebulae because of their distinctive spiral shape. In 1920, there was a “Great Debate” between astronomers Harlow Shapley and Heber Curtis questioning whether the spiral nebulae were part of our own Milky Way galaxy or were “island universes” beyond our Milky Way. Do you think the nebulae you’ve observed are within the Milky Way or beyond it?
            </p>
          </div>
          <div
            class="mb-2 mx-4"
          >    
            <v-row>
              <v-col
                cols="8"
                offset-lg="1"
              >   
                <c-exploration-tool3 id="exploration-tool3">
              </v-col>
              <v-col
                cols="4"
                lg="2"
              >
                <v-row
                  justify="space-between"
                >
                  <v-col
                    cols="12"
                    lg="6"
                  >
                    <v-btn
                      @click="go_to_location_tool3({
                          ra: 83.63,
                          dec: 22.014,
                          fov: 350, // optional, in arcseconds, default is 90
                          instant: false // also optional, false by default
                        })"
                      color="info"
                      width="100%"
                      class="mx-2"
                    >
                      M1
                    </v-btn>
                  </v-col>
                  <v-col
                    cols="12"
                    lg="6"
                  >
                    <v-btn
                      @click="go_to_location_tool3({
                          ra: 250.4,
                          dec: 36.46,
                          fov: 700, // optional, in arcseconds, default is 90
                          instant: false // also optional, false by default
                        })"
                      color="info"
                      width="100%"
                      class="mx-2"
                    >
                      M13
                    </v-btn>
                  </v-col>
                  <v-col
                    cols="12"
                    lg="6"
                  >
                    <v-btn
                      @click="go_to_location_tool3({
                          ra: 10.63,
                          dec: 41.27,
                          fov: 6000, // optional, in arcseconds, default is 90
                          instant: false // also optional, false by default
                        })"
                      color="info"
                      width="100%"
                      class="mx-2"
                    >
                      M31
                    </v-btn>
                  </v-col>
                  <v-col
                    cols="12"
                    lg="6"
                  >
                    <v-btn
                      @click="go_to_location_tool3({
                          ra: 83.82,
                          dec: -5.39,
                          fov:7500, // optional, in arcseconds, default is 90
                          instant: false // also optional, false by default
                        })"
                      color="info"
                      width="100%"
                      class="mx-2"
                    >
                      M42
                    </v-btn>
                  </v-col>
                  <v-col
                    cols="12"
                    lg="6"
                  >
                    <v-btn
                      @click="go_to_location_tool3({
                          ra: 202.47,
                          dec: 47.195,
                          fov: 700, // optional, in arcseconds, default is 90
                          instant: false // also optional, false by default
                        })"
                      color="info"
                      width="100%"
                      class="mx-2"
                    >
                      M51
                    </v-btn>
                  </v-col>
                  <v-col
                    cols="12"
                    lg="6"
                  >
                    <v-btn
                      @click="go_to_location_tool3({
                          ra: 148.97,
                          dec: 69.68,
                          fov: 400, // optional, in arcseconds, default is 90
                          instant: false // also optional, false by default
                        })"
                      color="info"
                      width="100%"
                      class="mx-2"
                    >
                      M82
                    </v-btn>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </div>     
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
      <!-- first button below just being used for testing, delete when using live with students -->
      <v-btn
        :class="step < 6 ? 'd-block' : 'd-none'"
        color="error"
        class="black--text"
        depressed
        @click="() => { 
          intro_complete = true;
          step = 0;
        }"
      >
        get started
      </v-btn>
      <v-btn
        :disabled="step > 6"
        :class="step >= 6 ? 'd-block' : 'd-none'"
        color="accent"
        class="black--text"
        depressed
        @click="() => { 
          intro_complete = true;
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
  transition: none !important;
}
#slideshow-root .v-card__text{
  padding: 0px 15px 0px;
  min-height: 550px;
}

#exploration-tool, #exploration-tool2, #exploration-tool3 {
  height: 400px;
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
