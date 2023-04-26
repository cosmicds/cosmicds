<template>
  <v-card
    flat
    :class="classes"
  >
    <v-toolbar
      color="primary"
      dense
      dark
      v-if="show_toolbar">
      <v-toolbar-title
        class="text-h6 text-uppercase font-weight-regular"
      >
        {{ title }}
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <jupyter-widget :widget="controls.toolbar_selection_tools"></jupyter-widget>
      </v-toolbar-items>
    </v-toolbar>
    <jupyter-widget class="viewer-widget" :style="css_style" :widget="figure"></jupyter-widget>
  </v-card>
</template>

<script>
module.exports = {
  data() {
    return {
      resizeObserver: null
    }
  },
  mounted() {
    this.resizeObserver = new ResizeObserver((entries, _observer) => {
      entries.forEach((entry) => {
        const el = entry.target;
        const viewerWidget = el.querySelector(".viewer-widget");
        if (!viewerWidget) {
          return;
        }
        this.viewer_height = viewerWidget.clientHeight;
        this.viewer_width = viewerWidget.clientWidth;
      });
    });

    this.resizeObserver.observe(this.$el);
  }
}
</script>
