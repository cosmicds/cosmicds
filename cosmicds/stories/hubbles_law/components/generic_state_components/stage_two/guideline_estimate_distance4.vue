<template>
  <scaffold-alert
    header-text="Estimate Distance"
    @back="
      state.marker = 'est_dis3';
    "
    @next="
      state.marker = 'fil_rem1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Enter the angular size of your galaxy in the box and click calculate to estimate the distance.
      </p>
      <p>
        MathJax stuff2
      </p>
    </div>
  </scaffold-alert>
</template>
