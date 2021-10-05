<template>
  <v-card>
    <v-card-title v-if="use_search">
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      v-model="selected"
      :headers="headers"
      :items="items"
      :search="search"
      :single-select="single_select"
      :item-key="key_component"
      show-select
      hide-default-footer
    >
    </v-data-table>
  </v-card>
</template>

<script>
  export default {
    data () {
      return {
        search: '',
        headers: [],
      }
    },
  }
</script>
