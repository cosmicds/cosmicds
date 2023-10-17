<template>
  <v-card
    v-intersect.once="(entries) => updateFromEntries(entries)"
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
    <v-expand-transition>
      <v-card-text
        v-show="show_subtitle"
        class="subtitle"
      >
        {{ subtitle }}
      </v-card-text>
    </v-expand-transition>
    <jupyter-widget :style="css_style" :widget="figure"></jupyter-widget>
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
      this.updateFromEntries(entries);
    });

    this.resizeObserver.observe(this.$el);
  },
  methods: {
    updateFromEntries(entries) {
      entries.forEach((entry) => {
        const el = entry.target;
        this.updateViewerSizes(el);
      });
    },
    updateViewerSizes(root=null) {
      const el = root || this.$el;
      const viewerWidget = el.querySelector("rect.plotarea_events");
      if (!viewerWidget) {
        return;
      }
      const bbox = viewerWidget.getBoundingClientRect();
      this.viewer_height = Math.round(bbox.height);
      this.viewer_width = Math.round(bbox.width);    
    }
  }
}
</script>

<style scoped>
.subtitle {
  padding: 0px !important;
  font-size: 1rem;
  text-align: left;
  margin-left: 1rem;
}

.vuetify-styles .theme--dark.v-card>.v-card__text {
  color: white !important;
}

.vuetify-styles .theme--light.v-card>.v-card__text {
  color: black !important;
}
</style>
