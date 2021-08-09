<template>
  <v-btn
      color="primary"
      dark
      @click.stop="dialog = true"
  >
    {{ launch_button_text }}

    <v-dialog
        v-model="dialog"
        max-width="500"
    >
      <v-card>
        <v-card-title class="text-h5">
          {{ title_text }}
        </v-card-title>

        <v-card-text>
          {{ content_text }}
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
              color="green darken-1"
              text
              @click="accept_button_clicked"
          >
            {{ accept_button_text }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-btn>
</template>