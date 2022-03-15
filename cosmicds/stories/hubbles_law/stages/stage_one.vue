<template>
  <v-container>
    <v-row>
      <v-btn
        color="green"
        @click="select_galaxies();"
      >select 5 galaxies</v-btn>
    </v-row>
    <v-row>
      <v-col
        cols="6">
        <v-card
          color="info"
          class="pa-1">
          <c-selection-tool/>
          <!-- <v-card-actions>
            <v-btn @click="story_state.step_index += 1; story_state.step_complete = true">Next Step</v-btn>
          </v-card-actions> -->
        </v-card>
      </v-col>
      <v-col
        cols="6"
        class="galtable_column">
        <v-card
          :color="stage_state.marker == 'cho_row1' ? 'info' : 'none'"
          :class="stage_state.marker == 'cho_row1' ? 'pa-1' : 'pa-0'">
          <jupyter-widget :widget="widgets.galaxy_table"/>
        </v-card>
      </v-col>
    </v-row>
    <v-row
      :class="stage_state.marker == 'sel_gal1' || stage_state.marker == 'cho_row1' ? 'd-block' : 'd-none'">
      <c-select-galaxies-guidance
        v-if="stage_state.marker == 'sel_gal1'" />
      <c-choose-row-alert
        v-if="stage_state.marker == 'cho_row1'" />
    </v-row>
    <v-row>
      <v-col
        cols="6">
        <v-card
          color="info"
          class="pa-1"
          v-if="stage_state.spectrum_tool_visible"
          >
          <jupyter-widget :widget="viewers.spectrum_viewer"/>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <c-spectrum-guidance 
          v-if="stage_state.marker == 'mee_spe1'"/>
        <c-restwave-alert
          v-if="stage_state.marker == 'res_wav1'" />
        <c-obswave-alert
          v-if="stage_state.marker == 'obs_wave1'" />
        <c-remaining-gals-alert
          v-if="stage_state.marker == 'rep_rem1'" />

        <!-- This alert is temporary -->
        <v-alert
          :class="stage_state.waveline_set ? 'd-block' : 'd-none'"
          border="left"
          color="indigo"
          dark
          elevation="2"
          class="mb-12">
          <v-btn
            :disabled="!stage_state.waveline_set"
            class="white-text"
            color="green"
            @click="add_current_velocity()"
          >find velocity
          </v-btn>
        </v-alert>

        <c-nice-work-alert
          v-if="stage_state.marker == 'nic_wor1'" />

        <v-row>
          <v-col
            cols="6"
          >
            <!-- FORM DIALOG as template for reflections/MC -->
            <guide-specvel-windows
              button-text="info"
              close-text="done"
              @close="
                console.log('Done button was clicked.');
                stage_state.vel_win_unopened = 0;
              "
            >
            </guide-specvel-windows>
          </v-col>
          <v-col
            cols="6"
          >
            <span
              :class="stage_state.waveline_set ? 'd-block' : 'd-none'"
            >
              <!-- FORM DIALOG as template for reflections/MC -->
              <reflect-velocity-windows
                button-text="do"
                close-text="submit"
                @submit="
                  console.log('Submit button was clicked.');
                "
              >
              </reflect-velocity-windows>
            </span>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>
