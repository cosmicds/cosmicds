<template>
  <scaffold-alert
    :class="state.marker == 'res_wav2' ? 'd-block' : 'd-none'"
    header-text="Rest Wavelength"
    @back="
      state.marker = 'res_wav1';
    "
    @next="
      state.marker = 'obs_wav1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        One of the lines in your spectrum is labeled with an element symbol. Click the label to note the element line and its <strong>rest wavelength</strong> in your table.
      </p>
    </div>
  </scaffold-alert>
</template>
