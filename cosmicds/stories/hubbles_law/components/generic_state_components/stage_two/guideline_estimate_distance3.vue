<template>
  <scaffold-alert
    header-text="Estimate Distance"
    @back="
      state.marker = 'cho_row2';
    "
    @next="
      state.marker = 'est_dis4';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Enter the angular size of your galaxy in the box and click calculate to estimate the distance.
      </p>
      <p>
        MathJax stuff
      </p>
    </div>
  </scaffold-alert>
</template>
