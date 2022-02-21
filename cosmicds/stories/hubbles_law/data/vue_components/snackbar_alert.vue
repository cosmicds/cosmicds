<template>
  <v-alert
    text
    prominent
    color="green darken-2"
    icon="mdi-alert-octagram-outline"
    class="pa-5 my-2 text-body-2"
  >
    <div>
      <strong>Guide Snackbar</strong>
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