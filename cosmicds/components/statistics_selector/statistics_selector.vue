<template>
  <v-card
    flat
    variant="outlined"
    class="statistics-selector"
  >
    <v-list-item-group
      multiple
      v-model="selected"
    >
      <v-list-item
        v-for="(stat, index) in statistics"
        :key="index"
        :value="stat"
        inactive
      >
        <template v-slot:default="{ active }">
          <v-list-item-content
            class="font-weight-bold"
          >
            {{ capitalizeFirstLetter(stat) }}
          </v-list-item-content>

          <v-list-item-action>
            <v-checkbox
              :input-value="active"
              :color="colors[index]"
            />
          </v-list-item-action>
        </template>
      </v-list-item>
    </v-list-item-group>
  </v-card>
</template>

<script>
export default {
  methods: {
    capitalizeFirstLetter(text) {
      return text.charAt(0).toUpperCase() + text.slice(1);
    }
  }
}
</script>
