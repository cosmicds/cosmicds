<template>
  <scaffold-alert
    :class="state.marker == 'res_wav1' ? 'd-block' : 'd-none'"
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
        Let’s come back to your galaxy spectrum. Notice your spectrum has some bright spikes or faint dips.
      </p>
      <p>
        The bright spikes are <strong>emission lines</strong>.
      </p>
      <p>
        The faint dips are <strong>absorption lines</strong>.
      </p>
      <p>
        One of the lines in your spectrum is labeled with an element symbol. Click the label to note the element line and its <strong>rest wavelength</strong> in your table.
      </p>
    </div>
  </scaffold-alert>
</template>
