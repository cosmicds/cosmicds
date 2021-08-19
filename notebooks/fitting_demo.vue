<template>
  <v-app id="fitting-demo">
    <v-container
      style="height: 600px"
    >
      <v-row>
        <v-col
          cols="3"
          class="align-stretch"
        >
          <v-btn
            @click="fit_lines({
              'viewer_id': 'viewer'
              })"
            color="primary"
          >
          Each Student
          </v-btn>
          <v-btn
            @click="fit_lines({
              'viewer_id': 'viewer',
              'aggregate': true
              })"
            color="primary"
          >
          Aggregate (keep others)
          </v-btn>
          <v-btn
            @click="fit_lines({
              'viewer_id': 'viewer',
              'aggregate': true,
              'clear_others': true
              })"
            color="primary"
          >
          Aggregate (clear others)
          </v-btn>
          <v-btn
            @click="fit_lines({
              'viewer_id': 'viewer',
              'layers': [0]
              })"
            color="primary"
          >
          Red (keep others)
          </v-btn>
          <v-btn
            @click="fit_lines({
              'viewer_id': 'viewer',
              'layers': [0],
              'clear_others': true
              })"
            color="primary"
          >
          Red (clear others)
          </v-btn>
          <v-btn
            @click="fit_lines({
              'viewer_id': 'viewer',
              'layers': [1,2]
              })"
            color="primary"
          >
          Green & blue (keep)
          </v-btn>
          <v-btn
            @click="fit_lines({
              'viewer_id': 'viewer',
              'layers': [1,2],
              'clear_others': true
              })"
            color="primary"
          >
          Green & blue (clear)
          </v-btn>
          <v-btn
            @click="clear_lines('viewer')"
            color="primary"
          >
          Clear lines
          </v-btn>
        </v-col>
        <v-col>
          <v-lazy>
            <jupyter-widget
              :widget="viewers.viewer"
            ></jupyter-widget>
          </v-lazy>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>
