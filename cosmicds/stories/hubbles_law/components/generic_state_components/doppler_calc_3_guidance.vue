<template>
  <scaffold-alert
    header-text="Velocity Calculation"
    @back="
      state.marker = 'dop_cal2';
    "
    @next="
      state.marker = 'dop_cal3';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Click on a row in your table to select one of the galaxies. You will calculate the velocity for this galaxy using the Doppler equation.
      </p>
      <p>
        $$ v=c \left(\frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}}-1\right) $$
      </p>
    </div>
  </scaffold-alert>
</template>
