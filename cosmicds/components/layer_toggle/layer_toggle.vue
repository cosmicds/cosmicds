<template>
  <v-card
    flat
  >
    <v-list-item-group
      multiple
      v-model="selected"
    >
      <v-list-item
        v-for="(layer, index) in layers"
        :key="index"
        :value="index"
        inactive
      >
        <template v-slot:default="{ active }">
          <v-list-item-content>
            {{ layer.label }}
          </v-list-item-content>

          <v-list-item-action>
            <v-checkbox
              :input-value="active"
              :color="layer.color"
            />
          </v-list-item-action>
        </template>

      </v-list-item>

    </v-list-item-group>
  </v-card>
</template>
