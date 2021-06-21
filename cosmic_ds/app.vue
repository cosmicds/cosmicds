<template>
  <v-app id="cosmic-ds-app">
    <v-app-bar
      color="primary"
      dark
      shrink-on-scroll
      prominent
      src="https://cdn.eso.org/images/screen/eso1738b.jpg"
      fade-img-on-scroll
      scroll-target="#scrolling-techniques-4"
    >
      <template v-slot:img="{ props }">
        <v-img
          v-bind="props"
          gradient="to top right, rgba(100,115,201,.7), rgba(25,32,72,.7)"
        ></v-img>
      </template>

      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <v-toolbar-title>Hubble Data Story</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn>

      <v-menu bottom left>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon color="yellow" v-bind="attrs" v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item v-for="(item, i) in items" :key="i">
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <template v-slot:extension>
        <v-tabs align-with-title>
          <v-tab>Collect Galaxy Data</v-tab>
          <v-tab>Analysis Tools</v-tab>
          <v-tab>View Results</v-tab>
        </v-tabs>
      </template>
    </v-app-bar>

    <v-main id="scrolling-techniques-4" class="overflow-y-auto fill-height">
      <v-container class="fill-height">
        <v-card
          class="fill-height overflow-y-auto d-flex flex-column"
          style="width: 100%"
        >
          <v-stepper v-model="state.e1" class="fill-height elevation-0">
            <v-stepper-header>
              <v-stepper-step :complete="state.e1 > 1" step="1" editable>
                Collect Galaxy Data
              </v-stepper-step>

              <v-divider></v-divider>

              <v-stepper-step :complete="state.e1 > 2" step="2" editable>
                Analysis Tools
              </v-stepper-step>

              <v-divider></v-divider>

              <v-stepper-step :complete="state.e1 > 2" step="3" editable
                >View Results</v-stepper-step
              >
            </v-stepper-header>

            <v-stepper-items class="fill-height">
              <v-stepper-content step="1">
                <v-card
                  class="fill-height mb-12"
                  color="grey lighten-1 elevation-0"
                ></v-card>

                <v-btn color="primary" @click="state.e1 = 2"> Continue </v-btn>

                <v-btn text> Cancel </v-btn>
              </v-stepper-content>

              <v-stepper-content step="2">
                <v-card
                  class="fill-height mb-12"
                  color="grey lighten-1 elevation-0"
                ></v-card>

                <v-btn color="primary" @click="state.e1 = 3"> Continue </v-btn>

                <v-btn text> Cancel </v-btn>
              </v-stepper-content>

              <v-stepper-content step="3">
                <v-card
                  class="fill-height mb-12"
                  color="grey lighten-1 elevation-0"
                ></v-card>

                <v-btn color="primary" @click="state.e1 = 1"> Continue </v-btn>

                <v-btn text> Cancel </v-btn>
              </v-stepper-content>
            </v-stepper-items>
          </v-stepper>
          <v-card-actions>
            <v-btn color="primary" @click="state.e1 = 1"> Continue </v-btn>

            <v-btn text> Cancel </v-btn>
          </v-card-actions>
        </v-card>
      </v-container>
    </v-main>

    <v-footer color="primary lighten-1" padless>
      <v-row justify="center" no-gutters>
        <v-btn
          v-for="link in state.footer_link_items"
          :key="link"
          color="white"
          text
          rounded
          class="my-2"
        >
          {{ link }}
        </v-btn>
        <v-col class="primary lighten-2 py-4 text-center white--text" cols="12">
          {{ new Date().getFullYear() }} — <strong>CosmicDS Project</strong>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<style id="cosmic-ds-app">
html {
  margin: 0;
  padding: 0;
}

body {
  margin: 0;
  padding: 0;
}

.jupyter-widgets .jp-Cell .jp-CodeCell .jp-Notebook-cell .jp-mod-noInput {
  margin: 0;
  padding: 0;
}

#cosmic-ds-app {
  height: 100%;
}

#app {
  height: 100vh;
}

.card-outter {
  position: relative;
  padding-bottom: 50px;
}
.card-actions {
  position: absolute;
  bottom: 0;
}
.v-stepper__wrapper {
  height: 100%;
}
</style>