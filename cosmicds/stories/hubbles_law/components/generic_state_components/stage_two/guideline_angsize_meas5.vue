<template>
  <scaffold-alert
    header-text="Angular Size Measurement"
    @back="
      state.marker = 'ang_siz4';
    "
    @next="
      state.marker = 'ang_siz6';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Notice your galaxy’s angular size is now displayed in the table.
      </p>
      <p>
        You may adjust your measurement by clicking on the ends of the blue line and moving it to a new location.
      </p>
      <p>
        Click <strong>DO'S AND DONT'S</strong> for tips on how to ensure the most accurate results.
      </p>
    </div>
  </scaffold-alert>
</template>
