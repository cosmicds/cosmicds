<script>
export default {
  // mounted: () => {
  //   console.log("MOUNTED Doppler Calc 4");
  // },
  async mounted() {
    console.log("MOUNTED Doppler Calc 4");
    // Grab MathJax itself
    // We want to wait for it to finish loading, in case there are
    // any elements that need to be typeset on the initial screen
    await new Promise((resolve, reject) => {
      const mathJaxScript = document.createElement('script');
      mathJaxScript.async = false;
      mathJaxScript.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js";
      document.head.appendChild(mathJaxScript);
      mathJaxScript.onload = (_e) => resolve();
      mathJaxScript.onerror = (_e) => reject();
    });
    await MathJax.startup.promise;

    // Not all of our elements are initially in the DOM,
    // so we need to account for that in order to get MathJax
    // to render their formulae properly
    const mathJaxOpeningDelimiters = [ "$$", "\\(", "\\[" ];
    const containsMathJax = node => mathJaxOpeningDelimiters.some(delim => node.innerHTML.includes(delim));
    const elementToScan = node => node.nodeType === Node.ELEMENT_NODE;
    const mathJaxCallback = function(mutationList, _observer) {
      mutationList.forEach(mutation => {
        if (mutation.type === 'childList') {

          const needTypesetting = [];
          mutation.addedNodes.forEach(node => {
            if (elementToScan(node) && containsMathJax(node)) {
              needTypesetting.push(node);
            }
          });
          if (needTypesetting.length > 0) {
            MathJax.typesetPromise(needTypesetting);
          }

          const toClear = [];
          mutation.removedNodes.forEach(node => {
            if (elementToScan(node) && containsMathJax(node)) {
              toClear.push(node);
            }
          })
          if (toClear.length > 0) {
            MathJax.typesetClear(toClear);
          }
        }
      });
    }
    const observer = new MutationObserver(mathJaxCallback);
    const options = { childList: true, subtree: true };
    observer.observe(this.$el, options);
  },
}
</script>

<template>
  <p>Math Jax Support Loaded</p>
</template>