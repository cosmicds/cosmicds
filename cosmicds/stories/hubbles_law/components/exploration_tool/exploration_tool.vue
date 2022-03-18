<template>
  <div id="exploration-root">
    <jupyter-widget
      :widget="widget"
      id="exploration-widget"
    />
  </div>
</template>

<style scoped>
.p-Widget {
  height: 100% !important;
  width: 100% !important;
}
</style>
