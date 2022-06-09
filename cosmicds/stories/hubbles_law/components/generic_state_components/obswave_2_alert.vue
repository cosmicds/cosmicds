<template>
  <scaffold-alert
    header-text="Observed Wavelength"
    @back="
      state.marker = 'obs_wav1';
    "
    @next="
      state.marker = 'rep_rem1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        <strong>Tips:</strong> You can re-measure the wavelength as many times as you like. 
      </p>
      <p>  
        If you want even more precision in your measurement, zoom in to a specific wavelength range in the viewer using the <v-icon>mdi-select-search</v-icon> icon in the toolbar.
      </p>
    </div>
  </scaffold-alert>
</template>
