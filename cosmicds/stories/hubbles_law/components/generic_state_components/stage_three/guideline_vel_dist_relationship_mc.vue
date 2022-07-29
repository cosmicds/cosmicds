<template>
  <scaffold-alert
    header-text="Relationship Between Velocity and Distance"
    @back="
      state.marker = 'ran_mar4';
    "
    @next="
      state.marker = 'ran_mar6';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Based on the best-fit line for your data, how would you describe the general relationship between the velocities and distances for galaxies?
      </p>
      <v-container
        class="px-0"
        fluid
      >
        <p>The trend is:</p>
        <v-radio-group>
          <v-radio
            key="1"
            label="The velocity of galaxies are generally the same across all distances."
            value="1"
          ></v-radio>
          <v-radio
            key="2"
            label="Galaxies that are at a greater distance from us tend to have a larger velocity."
            value="2"
          ></v-radio>
          <v-radio
            key="3"
            label="Galaxies that are at a greater distance from us tend to have a smaller velocity."
            value="3"
          ></v-radio>
          <v-radio
            key="4"
            label="The velocity of galaxies appears to be random across all distances."
            value="4"
          ></v-radio>
        </v-radio-group>
      </v-container>
    </div>
  </scaffold-alert>
</template>
