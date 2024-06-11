<script>
export default {
  mounted() {

    window.plotlyPromise = new Promise((resolve, reject) => {
      // For RequireJS reasons we can't do the script tag approach that we use for e.g. MathJax
      // Doing that with Plotly gives this error: https://requirejs.org/docs/errors.html#mismatch
      require(["https://cdn.plot.ly/plotly-2.32.0.min.js"], function(plotly) {
        window.Plotly = plotly;
        resolve();
      },
      function(error) {
        reject();
      });

    });
  }
}
</script>

<template>
</template>
