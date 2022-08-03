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
      Introducing the Guidelines
    </h3>
    <div
      class="mb-4"
    >
      <p>
        You will explore your data through different representations, including spatial images, tables, spectrum graphs, and scatter plots.
      <p>
      </p>
        <strong>Guidelines</strong> for your exploration will appear in these orange boxes. Next to them you will find relevant data views, highlighted with an orange background.
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
            state.marker = 'sel_gal1'
          "
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>
