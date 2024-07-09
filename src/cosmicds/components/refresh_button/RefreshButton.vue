<template>
  <v-btn
    @click="() => {
      if (before_refresh) {
        before_refresh();
      }
      refresh();
    }"
  >
    {{ button_text }}
  </v-btn>
</template>

<script>
export default {
  methods: {
    refresh() {
      location.reload();
    }
  }
}
</script>
