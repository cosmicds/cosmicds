<template>
  <v-card
    width="100%"
  >
    <v-card-title>{{state.galaxy.name || ""}}</v-card-title>
    <v-card-text>
      <v-divider></v-divider>
      <v-list>
        <v-list-item-content>
          <v-list-item-title>{{state.galaxy.type || "--"}}</v-list-item-title>
          <v-list-item-subtitle>galaxy type</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-content>
          <v-list-item-title>100,000 light years</v-list-item-title>
          <v-list-item-subtitle>assumed size</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-content>
          <v-list-item-title>{{angular_height}}</v-list-item-title>
          <v-list-item-subtitle>field of view</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-content>
          <v-list-item-title>{{angular_size || "--"}}</v-list-item-title>
          <v-list-item-subtitle>measured angular size</v-list-item-subtitle>
        </v-list-item-content>
      </v-list>
    </v-card-text>
  </v-card>
</template>
