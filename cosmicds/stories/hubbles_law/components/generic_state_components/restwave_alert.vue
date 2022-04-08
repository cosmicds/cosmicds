<template>
  <scaffold-alert
    header-text="Rest Wavelength"
    @back="
      state.marker = 'mee_spe1';
    "
    @next="
      state.marker = 'res_wav2';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Let’s come back to your galaxy spectrum. Notice your spectrum has some bright spikes or faint dips.
      </p>
      <p>
        The bright spikes are <strong>emission lines</strong>.
      </p>
      <p>
        The faint dips are <strong>absorption lines</strong>.
      </p>
    </div>
  </scaffold-alert>
</template>
