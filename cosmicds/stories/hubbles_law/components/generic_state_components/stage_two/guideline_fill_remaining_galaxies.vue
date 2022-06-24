<template>
  <scaffold-alert
    header-text="Estimate Distance"
    @back="
      state.marker = 'est_dis4';
    "
    @next="
      state.marker = 'two_com1';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Click the <v-icon>mdi-spider-thread</v-icon> icon in the table toolbar to calculate the distances for the remaining galaxies.
      </p>
    </div>
  </scaffold-alert>
</template>
