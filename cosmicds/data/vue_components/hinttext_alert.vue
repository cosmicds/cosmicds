<template>
  <v-alert
    text
    prominent
    color="yellow darken-3"
    icon="mdi-more"
    class="pa-5 my-2 text-body-2"
  >
    <div>
      <strong>Hint Text</strong>
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