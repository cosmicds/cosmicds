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
    >
      <v-col
        cols="12"
        lg="6"
      >
        <c-guideline-intro-explore
          v-if="stage_state.marker == 'ran_mar1'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-observe-trends-mc
          v-if="stage_state.marker == 'ran_mar2'"
          v-intersect.once="scrollIntoView" />
        <c-guideline-trend-lines-draw
          v-if="stage_state.marker == 'ran_mar3'"
          v-intersect.once="scrollIntoView" />
        <v-btn
          block
        >PLACEHOLDER 1 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="6"
      >
        <jupyter-widget :widget="widgets.fit_table"/>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
    >
      <v-col
        cols="12"
        lg="6"
      >
        <v-btn
          block
        >PLACEHOLDER 2 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="6"
      >
        <jupyter-widget :widget="viewers.morphology_viewer"/>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
    >
      <v-col
        cols="12"
        lg="6"
      >
        <v-btn
          block
        >PLACEHOLDER 3 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="6"
      >
        <jupyter-widget :widget="viewers.fit_viewer"/>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
    >
      <v-col
        cols="12"
        lg="6"
      >
        <v-btn
          block
        >PLACEHOLDER 4 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="6"
      >
        <jupyter-widget :widget="viewers.comparison_viewer"/>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
    >
      <v-col
        cols="12"
        lg="6"
      >
        <v-btn
          block
        >PLACEHOLDER 5 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="6"
      >
        <jupyter-widget :widget="viewers.class_distr_viewer"/>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
    >
      <v-col
        cols="12"
        lg="6"
      >
        <v-btn
          block
        >PLACEHOLDER 6 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="6"
      >
        <jupyter-widget :widget="viewers.all_distr_viewer"/>
      </v-col>
    </v-row>
    <v-row
      class="d-flex align-stretch"
    >
      <v-col
        cols="12"
        lg="6"
      >
        <v-btn
          block
        >PLACEHOLDER 7 {{ stage_state.marker }}</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="6"
      >
        <jupyter-widget :widget="viewers.sandbox_distr_viewer"/>
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
