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

<script>
export default {
  watch: {
    selected(newValue, _oldValue) {
      console.log("In selected watcher");
      const selectedKeys = newValue.map(x => x[this.key_component]);
      const allKeys = this.items.map(x => x[this.key_component]);
      const indices = [];
      allKeys.forEach((key, index) => {
        if (selectedKeys.includes(key)) {
          indices.push(index);
        }
      });
      console.log(newValue);
      console.log(selectedKeys);
      console.log(allKeys);
      console.log(indices);
      const rows = Array.from(this.$el.querySelectorAll("tr"));
      rows.shift();
      for (const [index, row] of rows.entries()) {
        if (indices.includes(index)) {
          row.classList.add("v-data-table__selected");
        } else {
          row.classList.remove("v-data-table__selected");
        }
      }
    }
  }
}
</script>


<style scoped>
tr.v-data-table__selected {
  background-color: dodgerblue !important;
}
</style>

