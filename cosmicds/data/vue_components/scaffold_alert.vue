<template>             
  <v-alert
    :dark="state.darkmode"
    class="mb-4"
    :color="state.darkmode ? 'pink darken-2' : 'orange lighten-2'"
    elevation="6"
  >
    <h3
      class="mb-4"
    >
      {{ headerText }}
    </h3>
    <slot></slot>
    <v-divider
      class="my-4"
      color="white"
      style="opacity: 0.4"
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
          color="pink accent-1"
          light
          elevation="4"
          @click="() => { $emit('next'); }"
        >
          {{ nextText }}
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