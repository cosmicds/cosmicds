<template>             
  <v-card
    color="info"
    class="mb-4 mx-auto guideline"
    max-width="800"
    elevation="6"
  >
    <v-card-text>
      <v-row
        v-if="header"
      >
        <v-col
          cols="10"
        >
          <h3
            class="mb-4"
          >
            {{ header }}
          </h3>
        </v-col>
        <v-col
          align="right"
        >
          <speech-synthesizer/>
        </v-col>
      </v-row>
      <slot :advance="advance"></slot>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <v-row
        align="center"
        class="pa-1"
        no-gutters
      >
        <v-col
          v-if="allowBack"
          class="shrink"
        >
          <div
            style="font-size: 16px;"
          >
            <v-btn
              class="black--text"
              color="accent"
              elevation="2"
              @click="() => { $emit('back'); }"
            >
              back
            </v-btn>
          </div>
        </v-col>
        <v-col
          v-if="!header"
          class="mx-2 shrink"
        >
          <speech-synthesizer/>
        </v-col>
        <v-col
          v-else
          xl="8"
          sm="6"
        >
          <div
            style="font-size: 16px; border-left: solid 3px #FFD740; padding-left: 10px;"
          >
            <slot name="back-content"></slot>
          </div>
        </v-col>

        <v-spacer></v-spacer>

        <v-col
          v-if="advance"
          class="shrink"
        >
          <div
            style="font-size: 16px;"
          >
            <v-btn
              class="black--text"
              color="accent"
              elevation="2"
              @click="() => { $emit('next'); }"
            >
              {{ nextText }}
            </v-btn>
          </div>
        </v-col>
        <v-col
          v-else
          cols="6"
          class="shrink"
        >
          <div
            style="font-size: 16px; border-left: solid 3px #FFD740; padding-left: 10px;"
          >
            <slot
              name="before-next"
            >
            </slot>
          </div>
        </v-col>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<style scoped>

.theme--dark .v-card__text, .theme--dark .v-card__actions,
  .theme--dark .v-alert.trend-alert, .theme--dark .v-icon:not(.v-alert__icon, .mdi-piggy-bank){
  color: white!important;
}

.theme--light .v-card__text, .theme--light .v-card__actions,
  .theme--light .v-alert.trend-alert, .theme--light .v-icon:not(.v-alert__icon, .mdi-piggy-bank){
  color: black!important;
}

.v-alert {
  background-color: #000D!important;
}

.v-textarea .v-input__slot {
  background-color: #0001!important;
}

</style>

<script>
module.exports = {
  props: {
    allowBack: {
      type: Boolean,
      default: true
    },
    headerText: {
      type: [String, Function],
      default: null
    },
    nextText: {
      type: String,
      default: "next"
    },
    canAdvance: {
      type: Function
    },
    state: {
      type: Object
    }
  },
  computed: {
    advance() {
      return !this.canAdvance || this.canAdvance(this.state);
    },
    header() {
      if (this.headerText instanceof Function) {
        return this.headerText(this.state);
      } else {
        return this.headerText;
      }
    }
  }
};
</script>
