<template>
  <scaffold-alert
    header-text="Select Five Galaxies"
    @back="
      state.marker = 'mee_gui1';
    "
    @next="
      state.marker = 'sel_gal2';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        This is a view of the night sky, like the one you explored earlier. This view shows a more modern data set from the Sloan Digital Sky Survey (SDSS), which has collected imaging and spectral data for millions of galaxies. This Data Story will focus on a nearby subset of galaxies.
      </p>
    </div>
  </scaffold-alert>
</template>
