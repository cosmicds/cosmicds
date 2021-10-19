<template>
  <v-btn
      color="info"
      dark
      @click.stop="dialog = true"
  >
    <v-icon
      class="mr-4"
    >
      mdi-pen
    </v-icon>
    {{ buttonText }}

    <v-dialog
        v-model="dialog"
        max-width="500"
    >
      <v-card>
        <v-card-title class="text-h5">
          {{ titleText }}
        </v-card-title>

        <v-card-text>
          <slot></slot>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
              color="green darken-1"
              text
              @click="() => { $emit('close'); dialog = false } "
          >
            {{ closeText }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-btn>
</template>

<script>
module.exports = {
  props: ["buttonText", "titleText", "closeText"],
  data: function () {
    return {
      dialog: false,
    };
  },
};
</script>