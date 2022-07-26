<template>
  <v-btn-toggle
    v-model="active_tool_id"
    borderless
    class="transparent"
    >
    <v-tooltip
      v-for="[id, {tooltip, icon, disabled}] of Object.entries(tools_data)"
      :key="id"
      top>
      <template v-slot:activator="{ on }">
        <v-btn
          v-on="on"
          icon
          :value="id"
          :disabled="disabled"
        >
          <v-icon>{{ icon }}</v-icon>
        </v-btn>
      </template>
      <span>{{ tooltip }}</span>
    </v-tooltip>
  </v-btn-toggle>
</template>
