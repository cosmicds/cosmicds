<template>
  <scaffold-alert
    header-text="Angular Size Measurement"
    @back="
      state.marker = 'ang_siz1';
    "
    @next="
      state.marker = 'ang_siz3';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Click the <v-icon>mdi-ruler</v-icon> icon to activate the angular size measuring tool.
      </p>
    </div>
  </scaffold-alert>
</template>
