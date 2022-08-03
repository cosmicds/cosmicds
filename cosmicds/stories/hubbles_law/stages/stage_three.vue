<template>
  <v-container>
    <v-row v-if="show_team_interface">
      <v-col>
        <v-btn
          @click="console.log(stage_state)"
        >
          State
        </v-btn>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
      v-if="stage_state.table_show.includes(stage_state.marker)"
    >
      <v-col
        cols="12"
        lg="5"
      >
        <c-guideline-intro-explore
          v-if="stage_state.marker == 'ran_mar1'"
          v-intersect.once="scrollIntoView" />
        <v-btn
          block
        >PLACEHOLDER 1 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="7"
      >
        <v-card
          :color="stage_state.table_highlights.includes(stage_state.marker) ? 'info' : 'black'"
          :class="stage_state.table_highlights.includes(stage_state.marker) ? 'pa-1 my-n1' : 'pa-0'"
          outlined
        >
          <jupyter-widget :widget="widgets.fit_table"/>
        </v-card>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
      v-if="stage_state.all_galaxies_morph_plot_show.includes(stage_state.marker)"
    >
      <v-col
        cols="12"
        lg="5"
      >
        <v-btn
          block
        >PLACEHOLDER 2 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="7"
      >
        <v-card
          :color="stage_state.all_galaxies_morph_plot_highlights.includes(stage_state.marker) ? 'info' : 'black'"
          :class="stage_state.all_galaxies_morph_plot_highlights.includes(stage_state.marker) ? 'pa-1 my-n1' : 'pa-0'"
          outlined
        >
          <jupyter-widget :widget="viewers.morphology_viewer"/>
        </v-card>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
      v-if="stage_state.my_galaxies_plot_show.includes(stage_state.marker)"
    >
      <v-col
        cols="12"
        lg="5"
      >
        <c-guideline-observe-trends-mc
          v-if="stage_state.marker == 'ran_mar2'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-trend-lines-draw
          v-if="stage_state.marker == 'ran_mar3'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-best-fit-line
          v-if="stage_state.marker == 'ran_mar4'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-vel-dist-relationship-mc
          v-if="stage_state.marker == 'ran_mar5'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-expanding-universe
          v-if="stage_state.marker == 'ran_mar6'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-running-race-mc
          v-if="stage_state.marker == 'ran_mar7'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-vel-dist-runners
          v-if="stage_state.marker == 'ran_mar8'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-best-fit-galaxy
          v-if="stage_state.marker == 'ran_mar9'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-age-equation
          v-if="stage_state.marker == 'ran_mar10'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-my-age-measurement
          v-if="stage_state.marker == 'ran_mar11'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-shortcomings-reflect
          v-if="stage_state.marker == 'ran_mar12'"
          v-intersect.once="scrollIntoView" />
        <v-btn
          block
        >PLACEHOLDER 3 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="7"
      >
        <v-card
          :color="stage_state.my_galaxies_plot_highlights.includes(stage_state.marker) ? 'info' : 'black'"
          :class="stage_state.my_galaxies_plot_highlights.includes(stage_state.marker) ? 'pa-1 my-n1' : 'pa-0'"
          outlined
        >
          <jupyter-widget :widget="viewers.fit_viewer"/>
        </v-card>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
      v-if="stage_state.all_galaxies_plot_show.includes(stage_state.marker)"
    >
      <v-col
        cols="12"
        lg="5"
      >
        <v-btn
          block
        >PLACEHOLDER 4 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="7"
      >
        <v-card
          :color="stage_state.all_galaxies_plot_highlights.includes(stage_state.marker) ? 'info' : 'black'"
          :class="stage_state.all_galaxies_plot_highlights.includes(stage_state.marker) ? 'pa-1 my-n1' : 'pa-0'"
          outlined
        >
          <jupyter-widget :widget="viewers.comparison_viewer"/>
        </v-card>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
      v-if="stage_state.my_class_hist_show.includes(stage_state.marker)"
    >
      <v-col
        cols="12"
        lg="5"
      >
        <v-btn
          block
        >PLACEHOLDER 5 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="7"
      >
        <v-card
          :color="stage_state.my_class_hist_highlights.includes(stage_state.marker) ? 'info' : 'black'"
          :class="stage_state.my_class_hist_highlights.includes(stage_state.marker) ? 'pa-1 my-n1' : 'pa-0'"
          outlined
        >
          <jupyter-widget :widget="viewers.class_distr_viewer"/>
        </v-card>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
      v-if="stage_state.all_classes_hist_show.includes(stage_state.marker)"
    >
      <v-col
        cols="12"
        lg="5"
      >
        <v-btn
          block
        >PLACEHOLDER 6 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="7"
      >
        <v-card
          :color="stage_state.all_classes_hist_highlights.includes(stage_state.marker) ? 'info' : 'black'"
          :class="stage_state.all_classes_hist_highlights.includes(stage_state.marker) ? 'pa-1 my-n1' : 'pa-0'"
          outlined
        >
          <jupyter-widget :widget="viewers.all_distr_viewer"/>
        </v-card>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
      v-if="stage_state.sandbox_hist_show.includes(stage_state.marker)"
    >
      <v-col
        cols="12"
        lg="5"
      >
        <v-btn
          block
        >PLACEHOLDER 7 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="7"
      >
        <v-card
          :color="stage_state.sandbox_hist_highlights.includes(stage_state.marker) ? 'info' : 'black'"
          :class="stage_state.sandbox_hist_highlights.includes(stage_state.marker) ? 'pa-1 my-n1' : 'pa-0'"
          outlined
        >
          <jupyter-widget :widget="viewers.sandbox_distr_viewer"/>
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
