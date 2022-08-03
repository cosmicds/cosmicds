<template>
  <v-card
    id="distance-root"
  >
    <v-toolbar
      color="primary"
      dense
      dark
      class="text-uppercase"
    >
      <v-toolbar-title>Cosmic Sky Viewer</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-tooltip top>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon
            v-bind="attrs"
            v-on="on"
            :disabled="Object.keys(state.galaxy).length == 0"
            @click="flagged = true"
          >
            <v-icon>mdi-flag</v-icon>
          </v-btn>
        </template>
        Flag galaxy as missing image
      </v-tooltip>

      <v-btn icon>
        <v-icon>mdi-information-outline</v-icon>
      </v-btn>
    </v-toolbar>
    <div class="distance-content">
      <canvas
        v-show="measuring"
        class="distance-canvas"
        ref="canvas">
      </canvas>
      <canvas
        class="fov-canvas"
        ref="fovCanvas"
      ></canvas>
      <v-lazy>
        <jupyter-widget
          :widget="widget"
          class="wwt-widget"
        />
      </v-lazy>
      <v-tooltip
        top
        class="fab-tooltip"
        >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            fab
            dark
            bottom
            right
            absolute
            :color="measuring ? 'red' : 'success'"
            class="measuring-fab black--text"
            :ripple="false"
            v-bind="attrs"
            v-on="on"
            v-show="measuring_allowed && !view_changing && state.show_ruler"
            @click="toggle_measuring()">
            <v-icon>{{ measuring ? 'mdi-stop' : 'mdi-ruler' }}</v-icon>
          </v-btn>
        </template>
        {{ measuring ? 'Stop measuring' : 'Start measuring' }}
      </v-tooltip>
    </div>
  </v-card>
</template>

<script>
export default {
    
  mounted() {
    this.setup();
    this.reset();
    this.ranIntersectObserver = false;
    window.addEventListener('resize', this.handleResize);
    // We don't get a Window resize event when the canvas first appears
    // so we watch the canvas' dimensions instead
    const resizeObserver = new ResizeObserver(_entries => {
      this.handleResize();
    });

    // The two canvases have the same dimensions
    // so we only need to observe one
    resizeObserver.observe(this.canvas);
  },

  unmounted() {
    window.removeEventListener('resize', this.handleResize);
    resizeObserver.unobserve(this.canvas);
  },

  methods: {

    setup: function() {
      this.setupMeasuringCanvas();
      this.setupFOVCanvas();
    },

    // This stuff only needs to be done once
    setupMeasuringCanvas: function() {
      // Constants
      this.pointRadius = 2;
      this.grabRadius = 4;
      this.delta = 8;
      this.pointerClass = "pointer";
      this.grabClass = "grab";
      this.grabbingClass = "grabbing";

      // Get the canvas
      this.canvas = this.$refs.canvas;
      this.height = 400; // See the component CSS
      this.width = this.canvas.width;
      this.setupMeasuringCanvasContext();
    },

    setupFOVCanvas: function() {
      this.fovCanvas = this.$refs.fovCanvas;
      const parent = this.fovCanvas.parentElement;
      this.fovCanvas.width = parent.clientWidth;
      this.fovCanvas.height = parent.clientHeight;
      this.fovContext = this.fovCanvas.getContext('2d');
      this.fovContext.lineWidth = 3;
      this.fovContext.strokeStyle = 'lime';

      const leftPadding = 5;
      const verticalPadding = 5;
      const endcapLength = 10;
      const gapHeight = 26;
      const fontSize = 18;
      const font = `${fontSize}px monospace`;
      const endcapEndX = leftPadding + endcapLength;

      const verticalX = leftPadding + (endcapLength / 2);
      const fracDown = 0.5;
      const adjustY = 1;
      const midYTop = this.fovCanvas.height * fracDown - (gapHeight / 2) - adjustY;
      const midYBot = this.fovCanvas.height * fracDown + (gapHeight / 2) - adjustY;
      const bottomEndcapY = this.fovCanvas.height - verticalPadding;
      this.textCoordinates = [leftPadding, this.fovCanvas.height * fracDown + ((gapHeight - fontSize) / 2)];
      this.textRect = [0, midYTop, this.fovCanvas.width, gapHeight];

      this.fovContext.beginPath();
      this.fovContext.moveTo(leftPadding, verticalPadding);
      this.fovContext.lineTo(endcapEndX, verticalPadding);
      this.fovContext.stroke();

      this.fovContext.beginPath();
      this.fovContext.moveTo(verticalX, verticalPadding);
      this.fovContext.lineTo(verticalX, midYTop);
      this.fovContext.stroke();

      this.fovContext.beginPath();
      this.fovContext.moveTo(verticalX, midYBot);
      this.fovContext.lineTo(verticalX, bottomEndcapY);
      this.fovContext.stroke();

      this.fovContext.beginPath();
      this.fovContext.moveTo(leftPadding, bottomEndcapY);
      this.fovContext.lineTo(endcapEndX, bottomEndcapY);
      this.fovContext.stroke();

      this.fovContext.font = font;
      this.fovContext.fillStyle = 'white';
      if (this.fov_text) {
        this.updateFOVText();
      }
    },

    updateFOVText: function() {
      this.fovContext.clearRect(...this.textRect);
      this.fovContext.fillText(this.fov_text, ...this.textCoordinates);
    },

    // This needs to be done any time we want to reset the state
    reset: function() {
      this.startPoint = null;
      this.endPoint = null;
      this.onStart = false;
      this.onEnd = false;
      this.mouseDown = false;
      this.mouseMoving = false;
      this.shouldFollowMouse = false;
      this.lineCreated = false;
      this.measuredDistance = 0;
      this.measuring = false;

      // Set the canvas handlers
      this.canvas.onmousemove = null;
      this.canvas.onmousedown = this.addInitialPoint;
      this.canvas.onmouseup = this.addInitialPoint;

      // Clear the canvas, if necessary
      this.clearCanvas();
    },

    setupMeasuringCanvasContext: function() {
      this.context = this.canvas.getContext('2d');
      this.context.lineWidth = 3;
      this.context.strokeStyle = '#00e676';
    },

    addInitialPoint: function(event) {

      // If we haven't put the first point down
      const coordinates = this.position(event);
      if (this.startPoint == null) {
        this.startPoint = coordinates;
        this.drawPoint(this.startPoint, 1);
        this.canvas.onmousemove = (e) => this.lineFollow(e, false);

      // If we haven't put the second point down
      } else if (this.endPoint === null) {
        this.endPoint = coordinates;
        this.clearCanvas();
        this.drawLine(this.startPoint, this.endPoint);
        this.drawEndcaps(this.startPoint, this.endPoint);
        this.updateMeasuredDistance();
        this.canvas.onmousedown = this.handleMouseDown;
        this.canvas.onmouseup = this.handleMouseUp;
        this.canvas.onmousemove = this.handleMouseMove;
      }
      this.lineCreated = true;
    },

    handleMouseDown: function(event) {
      this.mouseDown = true;

      // If we aren't on one of the endpoints,
      // then we're done here
      if (!(this.onStart || this.onEnd)) {
        event.stopImmediatePropagation();
        return;
      }

      // To make things easier, we define the point that
      // isn't being modified as the 'start' point
      if (this.onStart) {
        const tempPoint = this.startPoint;
        this.startPoint = this.endPoint;
        this.endPoint = tempPoint;
      }
      this.clearCanvas();
      this.drawPoint(this.startPoint);
      this.canvas.classList.add(this.grabbingClass);
      this.shouldFollowMouse = true;

      // To avoid the line 'vanishing' when we grab an endpoint
      // we draw a line from the other point to where the mouse it
      this.drawLine(this.startPoint, this.position(event));
    },

    handleMouseUp: function(event) {
      this.mouseDown = false;
      if (this.shouldFollowMouse) {
        this.endPoint = this.position(event);
        this.clearCanvas();
        this.drawLine(this.startPoint, this.endPoint);
        this.drawEndcaps(this.startPoint, this.endPoint);
        this.updateMeasuredDistance();
      }
      this.canvas.classList.remove(this.grabbingClass);
      this.mouseMoving = false;
      this.shouldFollowMouse = false;
    },

    handleMouseMove: function(event) {
      this.mouseMoving = true;
      if (this.shouldFollowMouse && this.mouseDown) {
        this.lineFollow(event, true);
      } else {
        this.lookForEndpoints(event);
      }
    },

    rescalePoints: function(points, xRatio, yRatio) {
      points.forEach(point => {
        point[0] = point[0] * xRatio;
        point[1] = point[1] * yRatio;
      });
    },

    handleResize: function() {
      const oldWidth = this.canvas.width;
      const oldHeight = this.canvas.height;
      const referenceElement = this.canvas.parentElement;
      this.canvas.width = referenceElement.clientWidth;
      this.canvas.height = referenceElement.clientHeight;
      this.fovCanvas.width = referenceElement.clientWidth;
      this.fovCanvas.height = referenceElement.clientHeight;
      const newWidth = referenceElement.clientWidth;
      const newHeight = referenceElement.clientHeight;
      if (newWidth === 0 || newHeight === 0) {
        this.canvas.width = oldWidth;
        this.canvas.height = oldHeight;
        this.fovCanvas.width = oldWidth;
        this.fovCanvas.height = oldHeight;
        return;
      }
      this.width = newWidth;
      this.height = newHeight;

      // Update the measuring canvas
      this.setupMeasuringCanvasContext();
      if (this.startPoint && this.endPoint) {
        const xRatio = this.canvas.width / oldWidth;
        const yRatio = this.canvas.height / oldHeight;
        this.rescalePoints([this.startPoint, this.endPoint], xRatio, yRatio);
        this.drawLine(this.startPoint, this.endPoint);
        this.drawEndcaps(this.startPoint, this.endPoint);
        this.updateMeasuredDistance();
      }

      // Update the FOV canvas
      this.setupFOVCanvas();
    },

    position: function(event) {
      return [event.offsetX, event.offsetY];
    },

    clearCanvas: function() {
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    },

    drawPoint: function(coordinates, radius=this.pointRadius) {
      this.context.beginPath();
      this.context.arc(...coordinates, radius, 0, 2*Math.PI);
      this.context.fill();
    },

    drawLine: function(start, end) {
      this.context.beginPath();
      this.context.moveTo(...start);
      this.context.lineTo(...end);
      this.context.stroke();
    },

    lineFollow: function(event, requireMouseDown) {
      this.mouseMoving = true;
      if (requireMouseDown && !this.mouseDown) { return; }
      const coordinates = this.position(event);
      this.clearCanvas();
      this.drawPoint(this.startPoint);
      this.drawLine(this.startPoint, coordinates);
    },

    distanceSquared: function(p1, p2) {
      return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2;
    },

    slope: function(p1=this.startPoint, p2=this.endPoint) {
      if (!(p1 && p2)) { return undefined; }
      return (p2[1] - p1[1]) / (p2[0] - p1[0]);
    },

    perpSlope: function(p1=this.startPoint, p2=this.endPoint) {
      if (!(p1 && p2)) { return undefined; }
      return (p1[0] - p2[0]) / (p2[1] - p1[1]);
    },

    yIntercept: function(p1=this.startPoint, p2=this.endPoint) {
      if (!(p1 && p2)) { return undefined; }
      return p2[1] - this.slope(p1, p2) * p2[0];
    },

    drawEndcaps: function(p1, p2) {
      const mPerp = this.perpSlope(p1, p2);
      const endpts = [p1, p2];

      // We have to handle this a bit differently if the line is horizontal
      // since the perpendicular lines are of the form x=constant
      if (Math.abs(mPerp) === Infinity) {
        endpts.forEach(p => {
          const [x, y] = p;
          this.drawLine([x, y - this.delta], [x, y + this.delta]);
        });
        return;
      }

      // The points corresponding to x +/- d
      // have a distance delta from the endpoints
      const d = this.delta / Math.sqrt(1 + mPerp ** 2);

      // Draw the endcap through each point
      endpts.forEach(p => {
        const [x, y] = p;
        const nonXTerm = (y - mPerp * x);
        const xp = x + d;
        const yp = mPerp * xp + nonXTerm;
        const xm = x - d;
        const ym = mPerp * xm + nonXTerm;
        this.drawLine([xm, ym], [xp, yp]);
      });
    },

    lookForEndpoints: function(event) {
      const coordinates = this.position(event);
      const rsqStart = this.distanceSquared(coordinates, this.startPoint);
      const rsqEnd = this.distanceSquared(coordinates, this.endPoint);
      const grabRadiusSq = this.grabRadius ** 2;
      this.onStart = rsqStart <= grabRadiusSq;
      this.onEnd = rsqEnd <= grabRadiusSq;
      if (this.onStart || this.onEnd) {
        this.canvas.classList.add(this.grabClass);
      } else {
        this.canvas.classList.remove(this.grabClass);
      }
    },

    distance: function(p1=this.startPoint, p2=this.endPoint) {
      if (!(p1 && p2)) { return 0; }
      return Math.sqrt(this.distanceSquared(p1, p2));
    },

    updateMeasuredDistance: function() {
      this.measuredDistance = this.distance();
    },

    // Exposed to Jupyter

    jupyter_reset: function() {
      this.reset();
    },

    jupyter_update_text: function() {
      this.updateFOVText();
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

.distance-content {
  width: 100%;
  height: 400px;
}

.wwt-widget, .distance-canvas, .fov-canvas {
  height: 400px;
  width: 100%;
  position: absolute;
}

.wwt-widget .p-Widget, .wwt-widget iframe {
  height: 400px !important;
  width: 100% !important;
  z-index: 15;
}

.distance-canvas {
  background: transparent;
  z-index: 20;
  cursor: crosshair;
}

.fov-canvas {
  background: transparent;
  z-index: 30;
  pointer-events: none;
}

.pointer {
  cursor: pointer;
}

.grab {
  cursor: grab;
}

.grabbing {
  cursor: grabbing;
}

.measuring-fab {
  --margin: 15px;
  --card-padding: 16px;
  bottom: 0px !important;
  margin-bottom: var(--margin);
  margin-right: calc(var(--margin) - var(--card-padding));
  z-index: 25 !important;
}

.measuring-fab:hover:before, .measuring-fab:focus:before {
  display: none;
}

.fab-tooltip {
  z-index: 25 !important;
}
</style>
