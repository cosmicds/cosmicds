<template>
  <scaffold-alert
    header-text="Best Fit Line"
    @back="
      state.marker = 'ran_mar3';
    "
    @next="
      state.marker = 'ran_mar5';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Depending on how messy your dataset is, it may be tricky to draw a trendline. We can use a formula to calculate the <strong>best-fit line</strong>, no matter how messy your data are. Let’s see how the calculated best-fit line compares with your trend line.
      </p>
      <p>
        Click on the “Find Best Fit” button to find the best fit line.
      </p>
    </div>
  </scaffold-alert>
</template>
