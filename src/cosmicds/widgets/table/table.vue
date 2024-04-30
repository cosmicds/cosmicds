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
        <span v-html="title">  </span>
        <v-spacer></v-spacer>
        <v-text-field v-if="use_search"
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-tooltip
        v-for="[tool_id, tool] of Object.entries(tools)"
        :key="tool_id"
        top
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon
            v-bind="attrs"
            v-on="on"
            :disabled="tool.disabled || false"
            @click="() => { activate_tool(tool_id); }"
          >
            <v-icon>{{tool.icon}}</v-icon>
          </v-btn>
        </template>
        <p class="tooltip" v-html="tool.tooltip">  </p>
      </v-tooltip>
    </v-toolbar>
    <v-data-table
      dense
      v-model="selected"
      @click:row="(item, data) => handle_row_click(item, data)"
      @update:sort-by="(field) => update_sort_by(field)"
      :headers="headers"
      :items="items"
      :search="search"
      :single-select="single_select"
      :item-key="key_component"
      :style="cssVars"
      hide-default-footer
    >
    <!-- vuetify loop over headers and make them accept html -->
    <template 
      v-for="header in headers" 
      v-slot:[`header.${header.value}`]="{ header }"
    >
      <span v-html="header.text"> </span>
    </template>
   
    </v-data-table>
  </v-card>
</template>

<script>

export default {

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
          row.classList.add(this.selected_class);
        } else {
          row.classList.remove(this.selected_class);
        }
      }
    },

    jupyter_update_tool: function(tool) {
      this.$set(this.tools, tool.id, tool);
    },

  },

  watch: {
    selected(newValue, oldValue) {
      if (newValue === oldValue) return;
      this.updateStyling(newValue, this.sortBy);
    }
  },

  computed: {
    cssVars() {
      return {
        "--selected-color": this.sel_color
      }
    }
  }
}
</script>


<style scoped>
tr.v-data-table__selected {
  background-color: var(--selected-color) !important;
}

th.text-start.sortable {
  font-size: 14px;
}
</style>

