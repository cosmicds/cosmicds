<template>
  <scaffold-alert
    header-text="Runner's Velocities vs. Distances"
    @back="
      state.marker = 'ran_mar7';
    "
    @next="
      state.marker = 'ran_mar9';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        To return to this data story, if we graph the runners’ velocities vs. distance, the graph would look like this.
      </p>
      <p>
        Doesn’t this look a lot like your graph for the galaxies?
      </p>
    </div>
  </scaffold-alert>
</template>
