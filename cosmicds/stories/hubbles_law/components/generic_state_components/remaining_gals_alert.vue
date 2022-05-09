 <template> 
  <scaffold-alert
    header-text="Repeat for Remaining Galaxies"
    @back="
      state.marker = 'obs_wav2';
    "
    @next="
      state.marker = 'nic_wor1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Your measurement of the line’s observed wavelength is now recorded in the table for your selected galaxy.
      </p>
      <p>
        Go through each of the remaining galaxies in your table and repeat these measurements until you have recorded rest and observed wavelengths for each of your galaxies.
      </p>
    </div>
    </div>
  </scaffold-alert>
</template>
