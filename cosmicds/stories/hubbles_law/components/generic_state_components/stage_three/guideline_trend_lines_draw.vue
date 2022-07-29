<template>
  <scaffold-alert
    header-text="Trend Lines"
    @back="
      state.marker = 'ran_mar2';
    "
    @next="
      state.marker = 'ran_mar4';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Even when data are messy, it is possible to explore relationships between the quantities being graphed. Scientists do this by fitting a <strong>model</strong> to the data. Often, they start with a trend line. A <strong>trend line</strong> (or best-fit line) is a line that most accurately fits the data and minimizes the total distance between all the points and the line.
      </p>
      <p>
        Try drawing a trend line through your data points.
      </p>
    </div>
  </scaffold-alert>
</template>
