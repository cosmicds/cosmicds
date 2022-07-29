<template>
  <scaffold-alert
    header-text="Trends in the Data"
    @back="
      state.marker = 'ran_mar1';
    "
    @next="
      state.marker = 'ran_mar3';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Do you see any sort of trend in your data? Is there a relationship between the velocity and distance of the galaxy?
      </p>
      <v-container
        class="px-0"
        fluid
      >
        <v-radio-group>
          <v-radio
            key="1"
            label="Yes, I see a trend"
            value="1"
          ></v-radio>
          <v-radio
            key="2"
            label="No, I don’t see a trend"
            value="2"
          ></v-radio>
          <v-radio
            key="3"
            label="I can’t tell if there’s a trend"
            value="3"
          ></v-radio>
          <v-radio
            key="4"
            label="What’s a trend?"
            value="4"
          ></v-radio>
        </v-radio-group>
      </v-container>
    </div>
  </scaffold-alert>
</template>
