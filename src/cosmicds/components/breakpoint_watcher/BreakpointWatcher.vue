<script>
export default {
  name: "BreakpointWatcher",
  data() {
    return {
      previousBreakpoint: null,
      currentBreakpoint: null,
    }
  },
  mounted() {
    window.addEventListener("resize", this.onResize);
    this.onResize();
  },
  unmounted() {
    window.removeEventListener("resize", this.onResize);
  },
  methods: {
    onResize() {
      const h = window.innerHeight
      const w = window.innerWidth
      const bp = this.$vuetify.breakpoint.name

      if (this.previousBreakpoint !== bp) {
        this.previousBreakpoint = this.currentBreakpoint
        this.currentBreakpoint = bp

        this.set_breakpoint_info({
          height: h,
          width: w,
          breakpoint: bp,
        })
      }
    }
  },
}
</script>

<template>
</template>