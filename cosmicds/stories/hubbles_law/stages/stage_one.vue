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
          @click="console.log(stage_state)"
        >
          State
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col
        cols="12"
        lg="4"
      >
        <c-stage-one-start-guidance
          v-if="stage_state.marker == 'mee_gui1'" />
        <c-select-galaxies-alert
          v-if="stage_state.marker == 'sel_gal1'" />
        <c-select-galaxies-2-guidance
          v-if="stage_state.marker == 'sel_gal2'" />
        <v-btn
          v-if="stage_state.marker == 'sel_gal2' && stage_state.gals_total < stage_state.gals_max && show_team_interface"
          color="error"
          class="black--text"
          block
          @click="select_galaxies();"
        >select 5 galaxies</v-btn>
      </v-col>
      <v-col
        cols="12"
        lg="8"
      >
        <v-card
          :color="stage_state.marker == 'sel_gal1' || stage_state.marker == 'sel_gal2' ? 'info' : 'black'"
          :class="stage_state.marker == 'sel_gal1' || stage_state.marker == 'sel_gal2' ? 'pa-1 my-n1' : 'pa-0'"
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
      >
        <c-choose-row-guidance
          v-if="stage_state.marker == 'cho_row1'" />
        <c-doppler-calc-3-guidance
          v-if="stage_state.marker == 'dop_cal3'" /> 
        <c-doppler-calc-4-component
          v-if="stage_state.marker == 'dop_cal4' || stage_state.marker == 'dop_cal5'"/>
        <c-doppler-calc-5-slideshow
          v-if="stage_state.marker == 'dop_cal5'"/>
        <c-doppler-calc-6-component
          v-if="stage_state.marker == 'dop_cal6'"/> 
      </v-col>
      <v-col
        cols="12"
        lg="8"
        class="galtable_column"
      >
        <v-card
          :color="stage_state.marker == 'cho_row1' ? 'info' : 'black'"
          :class="stage_state.marker == 'cho_row1' ? 'pa-1 my-n1' : 'pa-0'"
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
        <c-spectrum-guidance 
          v-if="stage_state.marker == 'mee_spe1'" />
        <c-restwave-guidance
          v-if="stage_state.marker == 'res_wav1'" />
        <c-obswave-1-guidance
          v-if="stage_state.marker == 'obs_wav1'" />
        <c-obswave-2-alert
          v-if="stage_state.marker == 'obs_wav2'" />
        <c-remaining-gals-guidance
          v-if="stage_state.marker == 'rep_rem1'" />
        <c-nice-work-guidance
          v-if="stage_state.marker == 'nic_wor1'" />
        <c-doppler-calc-0-alert
          v-if="stage_state.marker == 'dop_cal0'" />
        <c-doppler-calc-1-alert
          v-if="stage_state.marker == 'dop_cal1'" />
        <c-doppler-calc-2-alert
          v-if="stage_state.marker == 'dop_cal2'" />
      </v-col>
      <v-col
        v-if="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1']"
        cols="12"
        lg="8"
      >
        <v-row>
          <v-col
            class="py-0"
          >
            <v-card
              :color="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1'] ? 'info' : 'black'"
              :class="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1'] ? 'pa-1 my-n1' : 'pa-0'"
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
            <c-spectrum-slideshow v-if="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1']" />
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
          <v-col
            cols="12"
          >
            <!-- This alert is temporary -->
            <v-btn
              v-if="show_team_interface && stage_state.velocity_button"
              :disabled="!stage_state.waveline_set"
              class="white-text px-a"
              width="100%"
              color="success"
              @click="
                add_current_velocity();
              "
            >
              find velocity
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>
