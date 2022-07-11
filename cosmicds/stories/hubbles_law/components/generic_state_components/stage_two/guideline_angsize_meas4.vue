<template>
  <scaffold-alert
    header-text="Angular Size Measurement"
    @back="
      state.marker = 'ang_siz3';
    "
    @next="
      state.marker = 'ang_siz5';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Click on one edge of your galaxy and drag to the other edge to set the bounds of your measurement.
      </p>
    </div>
  </scaffold-alert>
</template>
