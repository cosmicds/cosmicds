<template>
  <scaffold-alert
    header-text="Select a Galaxy"
    @back="
      state.marker = 'dop_cal2';
    "
    @next="
      state.marker = 'dop_cal4';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Click on a row in your table to select one of the galaxies.
      </p>
      <p>
        You will calculate the velocity for this galaxy using the Doppler equation.
      </p>
    </div>
  </scaffold-alert>
</template>


<style>

.JaxEquation .MathJax {
  margin: 0 auto 16px !important;
}

</style>