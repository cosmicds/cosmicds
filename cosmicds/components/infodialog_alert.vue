<template>
  <v-alert
    text
    prominent
    color="blue lighten-1"
    icon="mdi-lightbulb-group-outline"
    class="pa-5 my-2 text-body-2"
  >
    <div>
      <strong>Information Dialog</strong>
    </div>
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