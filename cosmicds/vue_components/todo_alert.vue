<template>
  <v-alert
    text
    prominent
    type="error"
    icon="mdi-wrench-outline"
    class="pa-5 my-2 text-body-2"
  >
    <slot></slot>
  </v-alert>
</template>

<script>
module.exports = {
  props: [],
  data: function () {
    return {
    };
  },
};
</script>