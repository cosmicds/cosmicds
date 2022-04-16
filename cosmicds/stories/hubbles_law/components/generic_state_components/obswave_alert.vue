<template>
  <scaffold-alert
    header-text="Observed Wavelength"
    @back="
      state.marker = 'res_wav1';
    "
    @next="
      state.marker = 'obs_wav2';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Hover your mouse in the Spectrum Viewer. A vertical measuring tool identifies the wavelength as you move the tool left and right.
      </p>
      <p>
        Align the measuring tool to the H-&alpha; or Mg I marker and click. This records the <strong>observed</strong> wavelength in your table.
      </p>
    </div>
  </scaffold-alert>
</template>
