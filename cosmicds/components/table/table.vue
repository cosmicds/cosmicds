<template>
  <v-card
    flat
  >
    <v-toolbar
      color="primary"
      dense
      dark
    >
      <v-toolbar-title
        class="text-h6 text-uppercase font-weight-regular"
        v-if="title"
      >
        {{ title }}
        <v-spacer></v-spacer>
        <v-text-field v-if="use_search"
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-toolbar-title>
    </v-toolbar>
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
