<template>
  <v-container>
            <!--
    <v-row>
      <v-col>
        <v-btn
          color="error"
          class="black--text"
          @click="console.dir(app_state.student)"
        >show student data</v-btn>
        -->
        <!--
        <v-btn
          color="error"
          class="black--text"
          @click="fill_data();"
        >fill data points</v-btn>
        <v-btn
          @click="console.log(stage_state)"
        >State</v-btn> 
      </v-col>
    </v-row>
    -->

    <v-row>
      <v-col
        cols="12"
        lg="4"
      >

            <!--
        <c-stage-one-start-guidance
          v-if="stage_state.marker == 'mee_gui1'" />
        <c-select-galaxies-alert
          v-if="stage_state.marker == 'sel_gal1'" />
        <c-select-galaxies-2-guidance
          v-if="stage_state.marker == 'sel_gal2'" />
          -->
      </v-col>
      <v-col
        cols="12"
        lg="8"
      >
      <!--
        <v-card
          :color="stage_state.marker == 'sel_gal1' || stage_state.marker == 'sel_gal2' ? 'info' : 'black'"
          :class="stage_state.marker == 'sel_gal1' || stage_state.marker == 'sel_gal2' ? 'pa-1' : 'pa-0'"
          outlined
        >
          <c-selection-tool/>
          <!-- <v-card-actions>
            <v-btn @click="story_state.step_index += 1; story_state.step_complete = true">Next Step</v-btn>
          </v-card-actions> 
        </v-card>
                  -->
      </v-col>
      <!--
    </v-row>
    <v-row>
      -->
      <v-col
        cols="12"
        lg="8"
        class="galtable_column"
      >
        <v-card
          :color="stage_state.marker == 'cho_row1' ? 'info' : 'black'"
          :class="stage_state.marker == 'cho_row1' ? 'pa-1' : 'pa-0'"
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
        <v-card
          class="pa-4"
          color="info"
          elevation="6"
        >
          <ul>
            <li>Zoom in to region around line</li>
            <li>Align vertical measuring tool to line and click to record wavelength and velocity</li>
            <li>If line looks incorrect (for example, if there does not appear to be a strong Mg-I line) click the flag.</li>
            <li>Repeat for all 5 galaxies and click "Go to Distance Measurement" to move on</li>            
          </ul>
        </v-card>
        <!--
        <c-spectrum-guidance 
          v-if="stage_state.marker == 'mee_spe1'"/>
        <c-restwave-alert
          v-if="stage_state.marker == 'res_wav1'" />
        <c-obswave-alert
          v-if="stage_state.marker == 'obs_wav1'" />
        <c-obswave-2-alert
          v-if="stage_state.marker == 'obs_wav2'" />
        <c-remaining-gals-alert
          v-if="stage_state.marker == 'rep_rem1'" />
        <c-nice-work-alert
          v-if="stage_state.marker == 'nic_wor1'" />
        <c-doppler-calc-1-alert
          v-if="stage_state.marker == 'dop_cal1'" />
        <c-doppler-calc-2-alert
          v-if="stage_state.marker == 'dop_cal2'" />    
          -->        
      </v-col>
      <v-col
        cols="12"
        lg="8"
      >
        <v-card
          v-if="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1']"
          :color="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1'] ? 'info' : 'black'"
          :class="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1'] ? 'pa-1' : 'pa-0'"
          outlined
        >
          <jupyter-widget :widget="viewers.spectrum_viewer_1"/>
        </v-card>
        <v-card
          v-if="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1']"
          :color="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1'] ? 'info' : 'black'"
          :class="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1'] ? 'pa-1' : 'pa-0'"
          outlined
        >
          <jupyter-widget :widget="viewers.spectrum_viewer_2"/>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="9">
      </v-col>
      <v-col cols="3">
        <v-btn
          class="white-text px-a"
          color="success"
          @click="
            story_state.stage_index = 2;
          "
        >
          Go to Distance Measurement
        </v-btn>        
      </v-col>
    </v-row>
    <!--
    <v-row>
      <v-col cols="12" lg="8" offset-lg="4">
        <v-row>
          <v-col
            cols="6"
          >
            <!-- This alert is temporary --
            <v-btn
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
          <v-col
            cols="3"
          >
            <!-- FORM DIALOG as template for reflections/MC --
            <c-spectrum-slideshow v-if="stage_state.indices[stage_state.marker] >= stage_state.indices['mee_spe1']" />
          </v-col>
          <v-col
            cols="3"
          >
            <span
              v-if="stage_state.waveline_set" 
            >
              <!-- FORM DIALOG as template for reflections/MC --
              <reflect-velocity-windows
                button-text="reflect"
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
            -->
  </v-container>
</template>
