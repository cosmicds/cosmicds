<template>
  <v-dialog
    v-model="dialog"
    max-width="800px"
    persistent
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        icon
        @click.stop="() => { dialog = true; }"
      >
        <v-icon>mdi-help-circle-outline</v-icon>
      </v-btn>
    </template>
    <v-card
        class="mx-auto elevation-2"
    >
      <v-toolbar
          color="secondary"
          dark
          dense
      >
        <v-toolbar-title
            class="text-h6 text-uppercase font-weight-regular"
            style="color: white;"
        >
          {{ title }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <span
            @click="() => { dialog=false}"
        >
          <v-btn
              icon
          >
            <v-icon>
              mdi-close
            </v-icon>
          </v-btn>
        </span>
      </v-toolbar>
      <v-card-text>
        <div v-if="hasImage">
          <v-row>
            <v-col
                cols="12"
                lg="6"
            >
              <p class="my-5">
                {{ content }}
              </p>
            </v-col>
            <v-col
                cols="12"
                lg="6"
            >
              <v-img
                  :src="image"
                  :alt-text="altText"
              ></v-img>
            </v-col>
          </v-row>
        </div>
        <div v-else>
          <p class="my-5">
            {{ content }}
          </p>
        </div>
      </v-card-text>
    </v-card>      
  </v-dialog>
</template>


