<template>
  <scaffold-alert
    header-text="Estimate Distance"
    @back="
      state.marker = 'est_dis1';
    "
    @next="
      state.marker = 'est_dis2';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Recall, if we assume a galaxy is the same size as our Milky Way galaxy, the distance to the galaxy can be found using:
      </p>
      <p>
        D (Distance in Mpc) = 6200 / galaxy angular size (theta in arcseconds).
      </p>
    </div>
  </scaffold-alert>
</template>
