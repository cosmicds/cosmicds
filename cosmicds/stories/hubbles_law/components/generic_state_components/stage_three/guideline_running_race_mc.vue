<template>
  <scaffold-alert
    header-text="A Running Race"
    @back="
      state.marker = 'ran_mar6';
    "
    @next="
      state.marker = 'ran_mar8';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        To understand Hubble’s thinking about this, let’s use the following situation as a model: Imagine runners in the middle of a race, where the runners are running at different speeds.
      </p>
      <p>
        In this diagram, runner A is running with a velocity of 4 km per hour and has run a distance of 12 km, while runner C is running faster with a velocity of 10 km per hour and has gone a distance of 30 km.
      </p>
      <p>
        Can you figure out how long ago the race started — the “age” of the race? (Assume each runner has maintained a consistent speed for the entire race).
      </p>
      <v-container
        class="px-0"
        fluid
      >
        <p>The race began:</p>
        <v-radio-group>
          <v-radio
            key="1"
            label="1/3 of an hour ago"
            value="1"
          ></v-radio>
          <v-radio
            key="2"
            label="3 hours ago"
            value="2"
          ></v-radio>
          <v-radio
            key="3"
            label="12 hours ago"
            value="3"
          ></v-radio>
          <v-radio
            key="4"
            label="75 hours ago"
            value="4"
          ></v-radio>
        </v-radio-group>
      </v-container>
    </div>
  </scaffold-alert>
</template>
