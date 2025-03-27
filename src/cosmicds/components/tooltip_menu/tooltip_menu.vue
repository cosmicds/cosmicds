<!-- filepath: /Users/jal194/github/cosmicds_dev/solara_tests/solara_test_tools/TooltipMenu.vue -->
<template>
  <div style="position: relative;">
    <v-menu
      :bottom="bottom"
      :left="left"
      :right="right"
      :top="top"
      :offset-y="offset_y"
      :offset-x="offset_x"
      :open-on-hover="open_on_hover"
      :close-on-content-click="close_on_content_click"
      :attach="attach"
    > 
      <jupyter-widget v-for="child in children" :key="child" :widget="child"></jupyter-widget>
      <template v-slot:activator="{ on, attrs }">
        <v-tooltip
          bottom
        >
          <template v-slot:activator="{ on: tooltipOn, attrs: tooltipAttrs }">
            <v-btn
              block
              icon
              v-bind="{...attrs, ...tooltipAttrs}"
              v-on="{...on, ...tooltipOn}"
            >
              <v-icon>{{ icon }}</v-icon>
            </v-btn>
          </template>
          <span>{{ tooltip }}</span>
        </v-tooltip>
      </template>
      <slot></slot>
    </v-menu>
  </div>
</template>

<script>
</script>

<style scoped>
/* Add any custom styles here if needed */
</style>
