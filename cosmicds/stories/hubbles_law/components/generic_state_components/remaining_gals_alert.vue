 <template> 
  <scaffold-alert
    header-text="Repeat for Remaining Galaxies"
    @back="
      state.marker = 'obs_wav1';
    "
    @next="
      state.marker = 'nic_wor1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Your measurement of the line’s observed wavelength is now recorded in the table.
      </p>
      <p>
        Repeat these measurements for your 4 remaining galaxies.
      </p>
    </div>

    <div class="text-center my-8">
      <v-btn
        class="black--text"
        color="success"
        elevation="2"
        @click="
          state.dist_snackbar = 0;
          state.marker_snackbar = 0;
          state.vel_snackbar = 0;
          state.data_ready_snackbar = 0;
          state.marker_snackbar = 1;
        "
      >
        repeat 4 times
      </v-btn>
    </div>
  </scaffold-alert>
</template>
