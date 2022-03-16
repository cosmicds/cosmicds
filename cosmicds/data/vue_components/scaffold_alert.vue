<template>             
  <v-alert
    class="mb-4"
    color="info"
    elevation="6"
    height="100%"
  >
    <h3
      class="mb-4"
    >
      {{ headerText }}
    </h3>
    <slot></slot>
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
          @click="() => { $emit('back'); }"
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      <v-col
        class="shrink"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="() => { $emit('next'); }"
        >
          next
        </v-btn>
      </v-col>
    </v-row>
  </v-alert>
</template>

<script>
module.exports = {
  props: ["headerText", "nextText"],
  data: function () {
    return {
    };
  },
};
</script>