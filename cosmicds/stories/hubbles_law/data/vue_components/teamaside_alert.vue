<template>
  <v-alert
    text
    prominent
    color="deep-purple lighten-3"
    icon="mdi-penguin"
    class="pa-5 my-2 text-body-2"
  >
    <div>
      <strong>Team Aside</strong>
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