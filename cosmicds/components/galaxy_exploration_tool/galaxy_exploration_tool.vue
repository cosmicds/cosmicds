<template>
<v-lazy>
  <div id="exploration-root">
    <jupyter-widget
      :widget="widget"
      id="exploration-widget"
    />
  </div>
</v-lazy>
</template>

<style scoped>
#exploration-widget .p-Widget, #exploration-widget iframe {
  height: 350px !important;
}
</style>

</template>

