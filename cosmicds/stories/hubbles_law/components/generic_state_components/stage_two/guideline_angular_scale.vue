<template>
  <scaffold-alert
    header-text="Angular Size Measurement"
    @back="
      state.marker = 'cho_row1';
    "
    @next="
      state.marker = 'ang_sca1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Your galaxy now appears in the sky viewer. 
      </p>
      <p>
        Notice that the angular scale of the sky viewer window changes as you zoom towards or away from  your galaxy.
      </p>
    </div>
  </scaffold-alert>
</template>
