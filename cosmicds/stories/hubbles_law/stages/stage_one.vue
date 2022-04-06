<template>
  <v-container>
    <v-row>
      <v-col>
        <v-btn
          color="green"
          @click="select_galaxies();"
        >select 5 galaxies</v-btn>
        <v-btn
          @click="console.log(stage_state)"
        >State</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        cols="12"
        lg="4"
      >
        <c-select-galaxies-guidance
          v-if="stage_state.marker == 'sel_gal1'" />
        <c-select-galaxies-2-guidance
          v-if="stage_state.marker == 'sel_gal2'" />
      </v-col>
      <v-col
        cols="12"
        lg="8"
      >
        <v-card
          :color="stage_state.marker == 'sel_gal1' || stage_state.marker == 'sel_gal2' ? 'info' : 'black'"
          class="pa-1"
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
      >
        <c-choose-row-guidance
          v-if="stage_state.marker == 'cho_row1'" />
      </v-col>
      <v-col
        cols="12"
        lg="8"
        class="galtable_column"
      >
        <v-card
          :color="stage_state.marker == 'cho_row1' ? 'info' : 'black'"
          class="pa-1"
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
        <c-spectrum-guidance 
          v-if="stage_state.marker == 'mee_spe1'"/>
        <c-restwave-alert
          v-if="stage_state.marker == 'res_wav1'" />
        <c-restwave-2-alert
          v-if="stage_state.marker == 'res_wav2'" />
        <c-obswave-alert
          v-if="stage_state.marker == 'obs_wav1'" />
        <c-remaining-gals-alert
          v-if="stage_state.marker == 'rep_rem1'" />
        <c-nice-work-alert
          v-if="stage_state.marker == 'nic_wor1'" />
      </v-col>
      <v-col
        cols="12"
        lg="8"
      >
        <v-card
          color="info"
          class="pa-1"
          v-if="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1']"
        >
          <jupyter-widget :widget="viewers.spectrum_viewer"/>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" lg="8" offset-lg="4">
        <v-row>
          <v-col
            cols="6"
          >
            <!-- This alert is temporary -->
            <v-btn
              :disabled="!stage_state.waveline_set"
              class="white-text px-a"
              width="100%"
              color="green"
              @click="
                add_current_velocity();
              "
            >
              find velocity
            </v-btn>
          </v-col>
          <v-col
            cols="3"
          >
            <!-- FORM DIALOG as template for reflections/MC -->
            <c-spectrum-slideshow />
          </v-col>
          <v-col
            cols="3"
          >
            <span
              v-if="stage_state.waveline_set"
            >
              <!-- FORM DIALOG as template for reflections/MC -->
              <reflect-velocity-windows
                button-text="do"
                close-text="submit"
                @submit="
                  stage_state.marker = story_state.stage_index = 2;
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
