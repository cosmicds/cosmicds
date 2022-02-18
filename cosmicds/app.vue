<template>
  <v-app id="inspire">
    <v-app-bar
        app
        color="primary"
        dark
        src="https://cdn.eso.org/images/screen/eso1738b.jpg"
        clipped-right
        flat
        height="72"
    >
      <template v-slot:img="{ props }">
        <v-img
            v-bind="props"
            gradient="to top right, rgba(100,115,201,.7), rgba(25,32,72,.7)"
        ></v-img>
      </template>

      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title class="mr-5">
        <h2>Hubble's Law</h2>
      </v-toolbar-title>

      <v-toolbar-title> Cosmic Data Stories</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-responsive max-width="156">
        <v-text-field
            dense
            flat
            hide-details
            rounded
            solo-inverted
        ></v-text-field>
      </v-responsive>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app width="300">
      <!-- TODO: This should be a built-in prop, but border radius requires explicit style def... -->
      <v-sheet height="72" width="100%" style="border-radius: 0px">
        <v-list class="ma-0 pa-0">
          <v-list-item>
            <v-list-item-action>
              <v-avatar color="indigo">
                <v-icon dark> mdi-account-circle</v-icon>
              </v-avatar>
            </v-list-item-action>

            <v-list-item-content>
              <v-list-item-title>Nicholas Earl</v-list-item-title>
              <v-list-item-subtitle
              >nearl@gluesolutions.io
              </v-list-item-subtitle
              >
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-sheet>

      <!-- List of stages for this story -->
      <v-stepper
          v-model="story_state.stage_index"
          vertical
          flat
          non-linear
          class="elevation-0"
          @change="story_state.step_index = story_state.stages[story_state.stage_index].step_index"
      >
        <template v-for="(stage, key, index) in story_state.stages">
          <v-stepper-step
              :key="index"
              :complete="story_state.stage_index > index"
              :step="index"
              editable
          >
            {{ stage.title }}
            <small>{{ stage.subtitle }}</small>
          </v-stepper-step>

          <v-stepper-content :key="index" :step="index" class="my-0 py-0">
            <!-- Section containing each stage's individual steps -->
            <v-list dense nav>
              <v-list-item-group
                  v-model="story_state.step_index"
                  color="primary"
              >
                <v-list-item
                    v-for="(step, i) in story_state.stages[key].steps"
                    :key="i"
                >
                  <v-list-item-action>
                    <template v-if="step.completed">
                      <v-icon>mdi-checkbox-marked-circle</v-icon>
                    </template>
                    <template v-else>
                      <v-icon>mdi-checkbox-blank-circle-outline</v-icon>
                    </template>
                  </v-list-item-action>

                  <v-list-item-content>
                    <v-list-item-title>{{ step.title }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-stepper-content>
        </template>
      </v-stepper>
    </v-navigation-drawer>

    <v-navigation-drawer
        app
        clipped
        right
        permanent
        expand-on-hover
    >
      <v-list
          nav
          dense
      >
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-folder</v-icon>
          </v-list-item-icon>
          <v-list-item-title>My Files</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Shared with me</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-star</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Starred</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-content>
        <v-container fluid>
          <v-tabs-items v-model="story_state.stage_index">
            <v-tab-item
                v-for="(stage, key, index) in story_state.stages"
                :key="index"
            >
              <v-card flat>
                <v-card-title>{{ stage.title }}</v-card-title>
                <v-card-subtitle>{{ stage.subtitle }}</v-card-subtitle>
                <jupyter-widget :widget="stage.model_id"/>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-container>
      </v-content>
    </v-main>

    <v-footer app padless inset>
      <v-row justify="center" no-gutters>
        <v-col class="primary darken py-2 text-center white--text" cols="12">
          {{ new Date().getFullYear() }} — <strong>CosmicDS</strong>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script>
module.exports = {
  methods: {
    getCurrentStage: function () {
      return this.$data.story_state.stages[this.$data.story_state.stage_index];
    },
  },
};
</script>

<style id="cosmicds-app">
html,
body {
  margin: 0;
  padding: 0;
}

.jp-Notebook,
.jp-OutputArea-output,
.jupyter-widgets,
.jp-Cell,
.jp-CodeCell,
.jp-Notebook-cell,
.jp-mod-noInput,
.jp-Cell-outputWrapper {
  margin: 0;
  padding: 0;
}

#cosmicds-app {
  height: 100%;
}

#app {
  height: 100vh;
  margin: 0;
  padding: 0;
}

.bqplot {
  height: 100%;
}

.MathJax,
.MathJax_Display {
  width: fit-content;
  height: fit-content;
}

/* issues with empty headers pushing WWT widget south, anyone else having this problem? -HOH */
.wwt_column {
  overflow-y: hidden;
}

.wwt_widget .v-toolbar {
  display: none;
}
</style>
