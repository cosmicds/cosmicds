<template>
  <v-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
  >
    <h3
      class="mb-4"
    >
      Velocity Calculation
    </h3>
    <div
      class="mb-4"
      v-intersect="(entries, _observer, intersecting) => {
        if (!intersecting) return;
        const targets = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
        MathJax.typesetPromise(targets);            
      }"
      v-if="state.velocities_total < 5"
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
        Now that you know how to use the Doppler equation, click the <v-icon>mdi-run-fast</v-icon> icon in the table header to have the velocities of the remaining galaxies calculated as well.
      </p>
    </div>
    <div
      class="mb-4"
      v-if="state.velocities_total == 5"
    >
      Great work! You have completed Stage 1. Proceed to Stage 2.
    </div>   
    <v-divider
      class="my-4"
    >
    </v-divider>

    <v-row
      align="center"
      no-gutters
    >
      <v-col>
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'dop_cal3';
          "
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      
      <v-col
        cols="4"
        class="shrink"
        v-if="state.velocities_total < 5"
      >
        <div
          style="font-size: 16px;"
        >
          Click the <v-icon>mdi-run-fast</v-icon> icon.
        </div>
      </v-col>
      <v-col
        class="shrink"
        v-if="state.velocities_total == 5"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            story_state.stage_index = 2;
            story_state.step_complete = true"
          >
          stage 2
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>


<style>

.JaxEquation .MathJax {
  margin: 16px auto !important;
}

</style>
