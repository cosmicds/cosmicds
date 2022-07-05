<template>
  <scaffold-alert
    header-text="Estimate Distance"
    @back="
      state.marker = 'rep_rem1';
    "
    @next="
      state.marker = 'est_dis2';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Now that you have an angular size measurement for each galaxy, let’s estimate how far away they are.
      </p>
    </div>
  </scaffold-alert>
</template>
