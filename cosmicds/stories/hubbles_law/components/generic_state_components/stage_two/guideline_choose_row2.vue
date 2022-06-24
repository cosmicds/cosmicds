<template>
  <scaffold-alert
    header-text="Choose Galaxy"
    @back="
      state.marker = 'est_dis2';
    "
    @next="
      state.marker = 'est_dis3';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Click on a row to choose a galaxy whose distance we will estimate.
      </p>
    </div>
  </scaffold-alert>
</template>
