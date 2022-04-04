<template>
  <v-card>
    <v-card-title v-if="title">
      {{ title }}
      <v-spacer></v-spacer>
      <v-text-field v-if="use_search"
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      dense
      v-model="selected"
      @click:row="(item, data) => handle_row_click(item, data)"
      :headers="headers"
      :items="items"
      :search="search"
      :single-select="single_select"
      :item-key="key_component"
      hide-default-footer
    >
    </v-data-table>
  </v-card>
</template>

<style scoped>
tr.v-data-table__selected {
  background-color: dodgerblue !important;
}
</style>

