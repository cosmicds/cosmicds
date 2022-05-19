<template>
  <div
    id="selection-root"
    v-intersect.once="(entries, observer, isIntersecting) => {
      console.log('Here');
      const root = entries[0].target;
      const element = root.querySelector('iframe');
      console.log(element);
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
        Night Sky Viewer
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-tooltip top>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon
            v-bind="attrs"
            v-on="on"
            @click="reset()">
            <v-icon>mdi-home</v-icon>
          </v-btn>
        </template>
        Reset view
      </v-tooltip>

      <v-tooltip top>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon
            v-bind="attrs"
            v-on="on"
            :disabled="Object.keys(current_galaxy).length == 0"
            @click="mark_galaxy_bad()"
          >
            <v-icon>mdi-flag</v-icon>
          </v-btn>
        </template>
        Flag galaxy as missing image
      </v-tooltip>
      
      <v-btn
        icon
        @click.stop="dialog = true"
      >
        <v-icon>mdi-information-outline</v-icon>
      </v-btn>
      
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
              How to Use the Night Sky Viewer
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
          <v-card-text>
            <v-container>
              <v-row
              >
                <v-col>
                  <p>
                    The Night Sky Viewer shows a modern data set from the Sloan Digital Sky Survey (SDSS), which has collected imaging and spectral data for millions of galaxies. The green dots mark the locations of galaxies you can collect data for.
                  </p>
                  <v-row>
                    <v-col
                      cols="12"
                      lg="4"
                    >
                      <v-chip
                        label
                        outlined
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
      <canvas
          class="wwt-canvas"
          ref="canvas">
        </canvas>
        <v-lazy>
          <jupyter-widget
            :widget="widget"
            class="wwt-widget"
          />
        </v-lazy>
      <v-tooltip top>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            fab
            dark
            bottom
            right
            absolute
            color="secondary"
            class="selection-fab"
            v-bind="attrs"
            v-on="on"
            v-show="Object.keys(current_galaxy).length !== 0"
            @click="select_current_galaxy()">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </template>
        Add galaxy to my dataset
      </v-tooltip>
    </div>
  </div>
</template>

<script>
export default {
  
  mounted() {
    this.canvas = this.$refs.canvas;
    this.height = 400; // See the component CSS
    this.width = this.canvas.width;
    this.setupCanvas();

    window.addEventListener('resize', this.handleResize);
    // We don't get a Window resize event when the canvas first appears
    // so we watch the canvas' dimensions instead
    const resizeObserver = new ResizeObserver(_entries => {
      this.handleResize();
    });
    resizeObserver.observe(this.canvas);
  },

  methods: {

    setupCanvas: function() {
      this.context = this.canvas.getContext('2d');
      this.context.lineWidth = 3;
      this.context.strokeStyle = 'dodgerblue';

      const leftPadding = 5;
      const verticalPadding = 5;
      const endcapLength = 10;
      const gapHeight = 24;
      const fontSize = 16;
      const font = `${fontSize}px Arial`;
      const endcapEndX = leftPadding + endcapLength;

      const verticalX = leftPadding + (endcapLength / 2);
      const midYTop = (this.canvas.height - gapHeight) / 2;
      const midYBot = (this.canvas.height + gapHeight) / 2;
      const bottomEndcapY = this.canvas.height - verticalPadding;
      this.textCoordinates = [leftPadding, (this.canvas.height / 2) + ((gapHeight - fontSize) / 2)];
      this.textRect = [0, midYTop, this.canvas.width, gapHeight];

      this.context.beginPath();
      this.context.moveTo(leftPadding, verticalPadding);
      this.context.lineTo(endcapEndX, verticalPadding);
      this.context.stroke();

      this.context.beginPath();
      this.context.moveTo(verticalX, verticalPadding);
      this.context.lineTo(verticalX, midYTop);
      this.context.stroke();

      this.context.beginPath();
      this.context.moveTo(verticalX, midYBot);
      this.context.lineTo(verticalX, bottomEndcapY);
      this.context.stroke();

      this.context.beginPath();
      this.context.moveTo(leftPadding, bottomEndcapY);
      this.context.lineTo(endcapEndX, bottomEndcapY);
      this.context.stroke();

      this.context.font = font;
      this.context.fillStyle = 'dodgerblue';
      if (this.fov_text) {
        this.updateText();
      }
    },

    handleResize: function() {
      const oldWidth = this.canvas.width;
      const oldHeight = this.canvas.height;
      const referenceElement = this.canvas.parentElement;
      this.canvas.width = referenceElement.clientWidth;
      this.canvas.height = referenceElement.clientHeight;
      const newWidth = referenceElement.clientWidth;
      const newHeight = referenceElement.clientHeight;
      if (newWidth === 0 || newHeight === 0) {
        this.canvas.width = oldWidth;
        this.canvas.height = oldHeight;
        return;
      }
      this.canvas.width = newWidth;
      this.canvas.height = newHeight;
      this.width = newWidth;
      this.height = newHeight;
      this.setupCanvas();
    },

    updateText: function() {
      this.context.clearRect(...this.textRect);
      this.context.fillText(this.fov_text, ...this.textCoordinates);
    },

    jupyter_update_text: function() {
      this.updateText();
    }
  }
  
}
</script>


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

.wwt-widget, .wwt-canvas {
  height: 400px;
  width: 100%;
  position: absolute;
}

.wwt-canvas {
  background: transparent;
  z-index: 100;
  pointer-events: none;
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
