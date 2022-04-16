<template>
  <scaffold-alert
    header-text="Rest Wavelength"
    @back="
      state.marker = 'mee_spe1';
    "
    @next="
      state.marker = 'obs_wav1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Your galaxy spectrum has either an H-&alpha; emission line or a Mg-I absorption line marked.
      </p>
      <p>
        The known <strong>rest wavelength</strong> for the line is recorded in your table.
      </p>
      <p>
        Click the <v-icon>mdi-lambda</v-icon> icon in the viewer header to display the rest wavelength for that line. 
      </p>
    </div>
  </scaffold-alert>
</template>
