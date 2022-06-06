<template>
  <v-card
    id="selection-root"
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
      dense
      dark
    >
      <v-toolbar-title
        class="text-h6 text-uppercase font-weight-regular"
      >
        Cosmic Sky Viewer
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-tooltip top>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon
            v-bind="attrs"
            v-on="on"
            :disabled="Object.keys(current_galaxy).length == 0"
            @click="flagged = true"
          >
            <v-icon>mdi-flag</v-icon>
          </v-btn>
        </template>
        Flag galaxy as missing image
      </v-tooltip>

      <v-tooltip
        top
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            v-bind="attrs"
            v-on="on"
            @click.stop="dialog = true"
          >
            <v-icon>mdi-information-outline</v-icon>
          </v-btn>
        </template>
        Info for using this tool
      </v-tooltip>
      
      <v-dialog
          v-model="dialog"
          persistent
          max-width="1000px"
      >
        <v-card
          class="mx-auto"
        >
          <v-toolbar
            color="secondary"
            dense
            dark
          >
            <v-toolbar-title
              class="text-h6 text-uppercase font-weight-regular"
            >
              How to Use the Cosmic Sky Viewer
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <span
              @click="() => { $emit('close'); dialog = false; }"
            >
              <v-btn
                icon
              >
                <v-icon>
                  mdi-close
                </v-icon>
              </v-btn>
            </span>
          </v-toolbar>
          <v-card-text
            class="white black--text"
          >
            <v-container>
              <v-row
              >
                <v-col>
                  <p>
                    The Comsic Sky Viewer shows a modern data set from the Sloan Digital Sky Survey (SDSS), which has collected imaging and spectral data for millions of galaxies. The green dots mark the locations of galaxies you can collect data for.
                  </p>
                  <v-row>
                    <v-col
                      cols="12"
                      lg="4"
                    >
                      <v-chip
                        label
                        outlined
                        color="black"
                      >
                        Pan
                      </v-chip>
                    </v-col>
                    <v-col
                      cols="12"
                      lg="8"
                      class="pt-2"
                    >
                      <strong>click + drag</strong><br>
                      (or use <strong class="codeFont">I-J-K-L</strong> keys)
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col
                      cols="12"
                      lg="4"
                    >
                      <v-chip
                        label
                        outlined
                        color="black"
                      >
                        Zoom
                      </v-chip>
                    </v-col>
                    <v-col
                      cols="12"
                      lg="8"
                      class="pt-2"
                    >
                      <strong>scroll in and out</strong><br>
                      (or use <strong class="codeFont">Z-X</strong> keys)
                    </v-col>
                  </v-row>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>
      </v-dialog>

    </v-toolbar>
    <div class="selection-content">
        <v-lazy>
          <jupyter-widget
            :widget="widget"
            class="wwt-widget"
          />
        </v-lazy>
      <v-tooltip top>
        <template v-slot:activator="{ on, attrs }">
        <v-fab-transition>
          <v-btn
            fab
            dark
            bottom
            left
            absolute
            color="accent"
            class="selection-fab black--text"
            v-bind="attrs"
            v-on="on"
            v-show="Object.keys(current_galaxy).length !== 0"
            @click="select_current_galaxy()">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-fab-transition>
      </template>
      Add galaxy to my dataset
    </v-tooltip>
    <v-tooltip top>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          fab
          dark
          bottom
          right
          absolute
          color="accent"
          class="selection-fab black--text"
          v-bind="attrs"
          v-on="on"
          @click="reset()">
          <v-icon>mdi-cached</v-icon>
        </v-btn>
      </template>
      Reset view
    </v-tooltip>
  </v-card>
</template>

<style scoped>
#selection-root {
  --toolbar-height: 48px;
  --widget-height: 400px;
  height: calc(var(--toolbar-height) + var(--widget-height));
  width: 100%;
}

.selection-content {
  width: 100%;
  height: 400px;
}

.wwt-widget {
  height: 400px;
  width: 100%;
  position: absolute;
}

.selection-fab {
  --margin: 15px;
  --card-padding: 16px;
  bottom: 0px !important;
  margin-bottom: var(--margin);
  margin-right: calc(var(--margin) - var(--card-padding));
}

.wwt-widget .p-Widget, .wwt-widget iframe {
  height: 400px !important;
  width: 100% !important;
}
</style>
