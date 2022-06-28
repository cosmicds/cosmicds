<template>
  <v-alert
    text
    prominent
    color="pink darken-1"
    icon="mdi-head-snowflake"
    class="pa-5 my-2 text-body-2"
  >
    <div>
      <strong>Reflection Dialog</strong>
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