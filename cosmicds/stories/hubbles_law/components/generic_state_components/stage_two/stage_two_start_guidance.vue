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
      Stage Two Start
    </h3>
    <div
      class="mb-4"
    >
      <p>
        lorem ipsum
      <p>
      </p>
        lorem ipsum
      </p>
    </div>
    
    <v-divider
      class="my-4"
    >
    </v-divider>

    <v-row
      align="center"
      no-gutters
    >
      <v-spacer></v-spacer>
      <v-col
        class="shrink"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="
            state.marker = 'two_hol1'
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
