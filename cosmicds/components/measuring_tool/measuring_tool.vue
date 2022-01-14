<template>
  <div id="measurer-root">
    <canvas
      v-show="measuring"
      id="canvas"
      ref="canvas">
    </canvas>
    <jupyter-widget
      :widget="widget"
      id="widget"
    />
  </div>
</template>

<script>
export default {
    
  mounted() {
    this.setup();
    this.reset();
    window.addEventListener('resize', this.handleResize);
    // We don't get a Window resize event when the canvas first appears
    // so we watch the canvas' dimensions instead
    const resizeObserver = new ResizeObserver(_entries => {
      this.handleResize();
    });
    resizeObserver.observe(this.canvas);
  },

  unmounted() {
    window.removeEventListener('resize', this.handleResize);
    resizeObserver.unobserve(this.canvas);
  },

  methods: {

    // This stuff only needs to be done once
    setup: function() {
      // Constants
      this.pointRadius = 2;
      this.grabRadius = 4;
      this.delta = 8;
      this.pointerClass = "pointer";
      this.grabClass = "grab";
      this.grabbingClass = "grabbing";

      // Get the canvas
      this.canvas = this.$refs.canvas;
      this.setupCanvasContext();
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

    setupCanvasContext: function() {
      this.context = this.canvas.getContext('2d');
      this.context.lineWidth = 3;
      this.context.strokeStyle = 'dodgerblue';
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
      this.canvas.width = this.$el.clientWidth;
      this.canvas.height = this.$el.clientHeight;
      this.setupCanvasContext();
      if (this.startPoint && this.endPoint) {
        const xRatio = this.canvas.width / oldWidth;
        const yRatio = this.canvas.height / oldHeight;
        this.rescalePoints([this.startPoint, this.endPoint], xRatio, yRatio);
        this.drawLine(this.startPoint, this.endPoint);
        this.drawEndcaps(this.startPoint, this.endPoint);
      }
      if (this.canvas.width === 0 || this.canvas.height === 0) {
        this.reset();
      }
    },

    position: function(event) {
      return [event.offsetX, event.offsetY];
    },

    clearCanvas: function() {
      this.context.clearRect(0, 0, canvas.width, canvas.height);
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
  }
}
</script>

<style scoped>
#measurer-root {
  height: 400px;
  width: 100%;
  position: relative;
}

#widget {
  width: 100%;
  height: 100%;
  z-index: 15;
}

#canvas {
  background: transparent;
  z-index: 20;
}

#widget, #canvas {
  position: absolute;
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
</style>
