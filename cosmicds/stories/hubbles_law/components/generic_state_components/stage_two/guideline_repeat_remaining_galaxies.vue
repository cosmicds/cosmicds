<template>
  <scaffold-alert
    header-text="Repeat for Remaining Galaxies"
    @back="
      state.marker = 'ang_siz6';
    "
    @next="
      state.marker = 'rep_rem1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Repeat the angular size measurements for your remaining galaxies.
      </p>
    </div>
  </scaffold-alert>
</template>
