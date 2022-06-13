<template>
  <scaffold-alert
    header-text="Velocity Calculation"
    @back="
      state.marker = 'dop_cal3';
    "
    @next="
      state.marker = 'dop_cal4';
    "
  >
    <div
      class="mb-4"
      v-intersect="(entries, _observer, intersecting) => {
        if (!intersecting) return;
        const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
        MathJax.typesetPromise(targets);            
      }"
    >
      <p>
        Notice your calculated velocity is now entered in the table.
      </p>
      <div
        class="JaxEquation"
      >
        $$ v = {{ state.student_vel.toFixed(0).toLocaleString() }} \text{ km/s}$$ 
      </div>
      <p>
        Now that you know how to use the Doppler equation, click <strong>NEXT</strong> below to have the velocities of the remaining galaxies calculated as well.
      </p>
    </div>
  </scaffold-alert>
</template>


<style>

.JaxEquation .MathJax {
  margin: 16px auto !important;
}

</style>
