<template>
  <scaffold-alert
    header-text="Hubble's Expanding Universe"
    @back="
      state.marker = 'ran_mar5';
    "
    @next="
      state.marker = 'ran_mar7';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        The relationship between your galaxies’ velocity and distance is the same as what Hubble found: galaxies at a greater distance away are moving away from us at a higher velocity.
      </p>
      <p>
        This was a huge deal in 1920. This relationship that Hubble found serves as evidence that we live in an <strong>expanding universe</strong>. Hubble realized that an expanding universe implies that at some point all the galaxies were much closer together — "<strong>The Big Bang</strong>". The amount of time since The Big Bang tells us the <strong>age of the universe</strong>.
      </p>
    </div>
  </scaffold-alert>
</template>
