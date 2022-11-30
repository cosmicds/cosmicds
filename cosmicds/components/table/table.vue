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
      @update:sort-by="(field) => update_sort_by(field)"
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

<script>

export default {

  data: {
    selectedClass: "v-data-table__selected"
  },

  methods: {
    updateStyling: function(selected, sortBy) {
      const sortFunc = function(x,y) {
        if (x[sortBy] === y[sortBy]) return 0;
        if (x[sortBy] < y[sortBy]) return -1;
        return 1;
      }
      const selectedKeys = [...selected].sort(sortFunc).map(x => x[this.key_component]);
      const allKeys = [...this.items].sort(sortFunc).map(x => x[this.key_component]);
      const indices = [];
      allKeys.forEach((key, index) => {
        if (selectedKeys.includes(key)) {
          indices.push(index);
        }
      });
      const rows = Array.from(this.$el.querySelectorAll("tr"));
      rows.shift(); // The first row will be the header
      for (const [index, row] of rows.entries()) {
        if (indices.includes(index)) {
          row.classList.add(this.selectedClass);
        } else {
          row.classList.remove(this.selectedClass);
        }
      }
    }
  },

  watch: {
    selected(newValue, oldValue) {
      if (newValue === oldValue) return;
      this.updateStyling(newValue, this.sortBy);
    }
  }
}
</script>


<style scoped>
tr.v-data-table__selected {
  background-color: dodgerblue !important;
}
</style>

