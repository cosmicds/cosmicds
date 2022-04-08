<template>
  <scaffold-alert
    header-text="Observed Wavelength"
    @back="
      state.marker = 'res_wav1';
    "
    @next="
      state.marker = 'rep_rem1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Your line’s rest wavelength has been recorded in the table.
      </p>
      <p>
        Now let’s measure the <strong>observed wavelength</strong> of the line.
      </p>
      <p>
        Slide the vertical measuring tool until it aligns with the line you identified, and click to record the line’s observed wavelength in the table.
      </p>
    </div>
  </scaffold-alert>
</template>
