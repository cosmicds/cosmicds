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
        The distance estimate for your galaxy has been entered into the table.
      </p>
      <p>
        Click the <v-icon>mdi-tape-measure</v-icon> icon in the table toolbar to calculate distances for the remaining galaxies.
      </p>
    </div>
  </scaffold-alert>
</template>
