<template>
  <scaffold-alert
    header-text="Stage Two Holder"
    @back="
      state.marker = 'two_sta1';
    "
    @next="
      state.marker = 'two_hol1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        lorem ipsum
      </p>
      <p>
        lorem ipsum
      </p>
    </div>
  </scaffold-alert>
</template>
