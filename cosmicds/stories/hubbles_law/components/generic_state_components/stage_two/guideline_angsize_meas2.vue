<template>
  <scaffold-alert
    header-text="Angular Size Measurement"
    @back="
      state.marker = 'cho_row1';
    "
    @next="() => { state.show_ruler = true; state.marker = 'ang_siz3'; console.log(state.show_ruler) }"
  >
    <div
      class="mb-4"
    >
      <p>
        Your galaxy will appear in the sky viewer. (You may need to wait a few moments for the full-resolution image to load.)
      </p>
      <p>
        If you zoom towards or away from your galaxy, notice that the angular scale (marked by the green line) changes.
      </p>
    </div>
  </scaffold-alert>
</template>
