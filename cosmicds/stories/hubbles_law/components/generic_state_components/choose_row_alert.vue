<template>
  <scaffold-alert
    header-text="Choose a Row"
    @back="
        state.marker = 'sel_gal2';
    "
    @next="
        state.spectrum_tool_visible = 1;
        state.marker = 'mee_spe1';
    "
    >
    <div class="mb-4">
      <p>
      Let's take a look at the light spectrum for one of your galaxies.
      </p>
      <p>
      Click on a row in your table to choose that galaxy.
      </p>
    </div>
  </scaffold-alert>
</template>
