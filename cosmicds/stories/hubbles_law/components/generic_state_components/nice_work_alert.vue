<template>
  <scaffold-alert
    header-text="Nice Work"
    @back="
      state.marker = 'rep_rem1';
    "
    @next="
      state.marker = 'nic_wor1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        As scientists do, let’s examine what conclusions you might draw from your data.
      </p>
    </div>
  </scaffold-alert>
</template>
