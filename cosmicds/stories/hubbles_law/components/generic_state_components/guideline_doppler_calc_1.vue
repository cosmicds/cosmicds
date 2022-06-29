<template>
  <scaffold-alert
    header-text="Velocity Calculation"
    @back="
      state.marker = 'dop_cal0';
    "
    @next="
      state.marker = 'dop_cal2';
    "
  >
    <div
      class="mb-4"
    >  
      <p>
        You will use the Doppler equation to calculate the velocity for just one of your galaxies, so you get a feel for how it works.
      </p>
      <p>
        After that, we’ll fill in velocities for the rest of your galaxies for you.
      </p>
    </div>
  </scaffold-alert>
</template>
