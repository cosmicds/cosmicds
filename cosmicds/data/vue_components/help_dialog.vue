<template>
  <v-btn
      color="primary"
      dark
      @click.stop="dialog = true"
  >
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
              text
              @click="dialog = false"
          >
            {{ cancelText }}
          </v-btn>

          <v-btn
              color="green darken-1"
              text
              @click="() => { $emit('accept'); dialog = false } "
          >
            {{ acceptText }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-btn>
</template>

<script>
module.exports = {
  props: ["buttonText", "titleText", "acceptText", "cancelText"],
  data: function () {
    return {
      dialog: false,
    };
  },
};
</script>