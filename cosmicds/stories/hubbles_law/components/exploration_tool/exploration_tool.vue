<template>
  <v-card
    outlined
    color="info"
    class="pa-1"
    v-intersect.once="(entries, observer, isIntersecting) => {
      const root = entries[0].target;
      const element = root.querySelector('iframe');
      if (element) {
        element.src = element.src.replace('/api/kernels', '');
      }
    }"
  >
    <v-toolbar
      color="primary"
      height="40px"
      dense
      dark
      class="text-uppercase"
    >
      <v-toolbar-title>Cosmic Sky Viewer</v-toolbar-title>
      <v-spacer></v-spacer>          
      <div class="text-center">
        <v-dialog v-model="dialog" width="600">
          <template v-slot:activator="{ on, attrs }">
            <v-btn 
              icon
              right
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-information-outline</v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              Data Tool and Imagery credits
            </v-card-title>
            <v-card-text>
              lorem ipsum
            </v-card-text>
            <v-card-actions>
               <v-spacer></v-spacer>
              <v-btn
                text
                @click="dialog = false"
              >
                Close
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>
    </v-toolbar>         
    <div id="exploration-root">
      <jupyter-widget
        :widget="widget"
        id="exploration-widget"
      >
    </div>
  </v-card>
</template>

<style scoped>
#exploration-widget .p-Widget, iframe {
  height: 350px !important;
  width: 100% !important;
}
</style>
