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
        Click on one edge of your galaxy to mark the ruler's starting point.
      </p>
      <p>
        With the button held down, drag to the other edge of your galaxy and release the button.
      </p>
    </div>
  </scaffold-alert>
</template>
