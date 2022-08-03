<template>
  <v-container>
    <v-row v-if="show_team_interface">
      <v-col>
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
    <v-row
      class="d-flex align-stretch"
    >
      <v-col
        cols="12"
        lg="4"
      >
        <c-guideline-angsize-meas1
          v-if="stage_state.marker == 'ang_siz1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-angsize-meas2
          v-if="stage_state.marker == 'ang_siz2'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-angsize-meas3
          v-if="stage_state.marker == 'ang_siz3'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-angsize-meas4
          v-if="stage_state.marker == 'ang_siz4'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-angsize-meas5
          v-if="stage_state.marker == 'ang_siz5'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-angsize-meas6
          v-if="stage_state.marker == 'ang_siz6'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-repeat-remaining-galaxies
          v-if="stage_state.marker == 'rep_rem1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-estimate-distance1
          v-if="stage_state.marker == 'est_dis1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-estimate-distance2
          v-if="stage_state.marker == 'est_dis2'"
          v-intersect.once="scrollIntoView" />
      </v-col>
      <v-col
        cols="12"
        lg="8"
      >
        <v-row>
          <v-col
            class="py-0"
          >
            <v-card
              :color="stage_state.csv_highlights.includes(stage_state.marker) ? 'info' : 'black'"
              :class="stage_state.csv_highlights.includes(stage_state.marker) ? 'pa-1 my-n1' : 'pa-0'"
              outlined
            >
              <c-distance-tool />
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="6"
            offset="3"
          >
            <c-dosdonts-slideshow />
          </v-col>
        </v-row>
      </v-col>
      <v-col
        cols="12"
        lg="8"
        offset-lg="4"
        v-if="stage_state.distance_sidebar"
      >
        <c-distance-sidebar />
      </v-col>
    </v-row>
    <v-row>
      <v-col
        cols="12"
        lg="4"
      >
        <c-guideline-choose-row1
          v-if="stage_state.marker == 'cho_row1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-choose-row2
          v-if="stage_state.marker == 'cho_row2'"
          v-intersect.once="scrollIntoView" />    
        <c-guideline-estimate-distance3
          v-if="stage_state.marker == 'est_dis3'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-estimate-distance4
          v-if="stage_state.marker == 'est_dis4'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-fill-remaining-galaxies
          v-if="stage_state.marker == 'fil_rem1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-stage-two-complete
          v-if="stage_state.marker == 'two_com1'"
          v-intersect.once="scrollIntoView" />
      </v-col>
      <v-col
        cols="12"
        lg="8"
      >
        <v-card
          :color="stage_state.table_highlights.includes(stage_state.marker) ? 'info' : 'black'"
          :class="stage_state.table_highlights.includes(stage_state.marker) ? 'pa-1 my-n1' : 'pa-0'"
          outlined
        >
          <jupyter-widget :widget="widgets.distance_table" />
        </v-card>
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