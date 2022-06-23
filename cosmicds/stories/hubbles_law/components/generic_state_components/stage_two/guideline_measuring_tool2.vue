<template>
  <scaffold-alert
    header-text="Angular Size Measurement"
    @back="
      state.marker = 'ang_siz3';
    "
    @next="
      state.marker = 'ang_siz4';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Click on one edge of your galaxy to mark the ruler’s starting point.
      </p>
      <p>
        Drag to the other edge of your galaxy and click again.
      </p>
    </div>
  </scaffold-alert>
</template>
