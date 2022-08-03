<template>
  <v-container>
    <v-row v-if="show_team_interface">
      <v-col>
        <v-btn
          color="error"
          class="black--text"
          @click="fill_data();"
        >fill data points</v-btn>
        <v-btn
          @click="() => {
            console.log('stage state:', stage_state);
            console.log('story state:', story_state);
            }"
        >
          State
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col
        cols="12"
        lg="4"
        :style="$vuetify.breakpoint.lg ? 'max-height: 100px' : 'max-height: 2500px'"
      >
        <c-guideline-intro-guidelines
          v-if="stage_state.marker == 'mee_gui1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-select-galaxies-1
          v-if="stage_state.marker == 'sel_gal1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-select-galaxies-2
          v-if="stage_state.marker == 'sel_gal2' & stage_state.gals_total == 0"
          v-intersect.once="scrollIntoView" />
        <c-guideline-select-galaxies-3
          v-if="stage_state.marker == 'sel_gal3'"
          v-intersect.once="scrollIntoView" />
        <v-btn
          v-if="stage_state.marker == 'sel_gal2' || 'sel_gal3' && stage_state.gals_total < stage_state.gals_max && show_team_interface"
          color="error"
          class="black--text"
          block
          max-width="800"
          @click="select_galaxies();"
        >select 5 galaxies</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="8"
      >
        <v-card
          :color="stage_state.csv_highlights.includes(stage_state.marker) ? 'info' : 'black'"
          :class="stage_state.csv_highlights.includes(stage_state.marker) ? 'pa-1 my-n1' : 'pa-0'"
          outlined
        >
          <c-selection-tool/>
          <!-- <v-card-actions>
            <v-btn @click="story_state.step_index += 1; story_state.step_complete = true">Next Step</v-btn>
          </v-card-actions> -->
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        cols="12"
        lg="4"
        :style="$vuetify.breakpoint.lg ? 'max-height: 100px' : 'max-height: 2500px'"
      >
        <c-guideline-notice-galaxy-table 
          v-if="stage_state.marker == 'sel_gal2' & stage_state.gals_total == 1"
          v-intersect.once="scrollIntoView" />
        <c-guideline-choose-row
          v-if="stage_state.marker == 'cho_row1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-doppler-calc-3
          v-if="stage_state.marker == 'dop_cal3'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-doppler-calc-4
          v-if="stage_state.marker == 'dop_cal4' || stage_state.marker == 'dop_cal5'"
          v-intersect.once="scrollIntoView" />
        <c-slideshow-doppler-calc-5
          v-if="stage_state.marker == 'dop_cal5'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-doppler-calc-6
          v-if="stage_state.marker == 'dop_cal6'"
          v-intersect.once="scrollIntoView" />
      </v-col>
      <v-col
        cols="12"
        lg="8"
        class="galtable_column"
      >
        <v-card
          :color="stage_state.table_highlights.includes(stage_state.marker) ? 'info' : 'black'"
          :class="stage_state.table_highlights.includes(stage_state.marker) ? 'pa-1 my-n1' : 'pa-0'"
          outlined
        >
          <jupyter-widget :widget="widgets.galaxy_table"/>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        cols="12"
        lg="4"
      >
        <c-guideline-spectrum
          v-if="stage_state.marker == 'mee_spe1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-restwave
          v-if="stage_state.marker == 'res_wav1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-obswave-1
          v-if="stage_state.marker == 'obs_wav1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-obswave-2
          v-if="stage_state.marker == 'obs_wav2'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-remaining-gals
          v-if="stage_state.marker == 'rep_rem1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-reflect-on-data
          v-if="stage_state.marker == 'ref_dat1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-doppler-calc-0
          v-if="stage_state.marker == 'dop_cal0'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-doppler-calc-1
          v-if="stage_state.marker == 'dop_cal1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-doppler-calc-2
          v-if="stage_state.marker == 'dop_cal2'"
          v-intersect.once="scrollIntoView" />
      </v-col>
      <v-col
        v-if="stage_state.spec_viewer_reached"
        cols="12"
        lg="8"
      >
        <v-row>
          <v-col
            class="py-0"
          >
            <v-card
              :color="stage_state.spec_highlights.includes(stage_state.marker) ? 'info' : 'black'"
              :class="stage_state.spec_highlights.includes(stage_state.marker) ? 'pa-1 my-n1' : 'pa-0'"
              outlined
            >
              <jupyter-widget :widget="viewers.spectrum_viewer"/>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="4"
            offset="2"
          >
            <!-- LEARN MORE Dialog -->
            <c-spectrum-slideshow />
          </v-col>
          <v-col
            cols="4"
          >
            <!-- REFLECTION Dialog -->
            <reflect-velocity-windows
              v-if="stage_state.obswaves_total >= 5"
              button-text="reflect"
              close-text="submit"
              @submit="
                stage_state.reflection_complete = true;
                console.log('Submit button was clicked.');
              "
            >
            </reflect-velocity-windows>
            <!-- Placeholder for Reflection button -->
            <v-btn
              v-if="stage_state.obswaves_total < 5"
              disabled
              block
              color="info"
              elevation="2"
            >
              <v-spacer></v-spacer>
              reflect
              <v-spacer></v-spacer>
              <v-icon
                class="ml-4"
              >
                mdi-circle-outline
              </v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
module.exports = {
  methods: {
    scrollIntoView: function(entries, observer, isIntersecting) {
      if (isIntersecting) {
        entries[0].target.scrollIntoView({
          behavior: 'smooth',
          block: 'center'
        });
      }
    }
  }
}

</script>
