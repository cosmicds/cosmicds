<template>
  <scaffold-alert
    header-text="Angular Size Measurement"
    @back="
      state.marker = 'ang_siz5';
    "
    @next="
      state.marker = 'rep_rem1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        If necessary, click and drag the ends of the measurement tool to make adjustments
      </p>
      <p>
        The table will update to display your most recent angular size measurement.
      </p>
    </div>
  </scaffold-alert>
</template>
