<template>             
  <v-card
    color="info"
    class="mb-4 mx-auto guideline"
    elevation="6"
  >
    <v-card-text>
      <h3
        v-if="header"
        class="mb-4"
      >
        {{ header }}
      </h3>
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
              ref="back"
              @click="() => { $emit('back'); }"
            >
              back
            </v-btn>
          </div>
        </v-col>
        <v-col
          v-else
          class="mx-2 shrink"
        >
          <speech-synthesizer/>
        </v-col>
        <v-col
          v-if="allowBack"
          class="mx-2 shrink"
        >
          <speech-synthesizer/>
        </v-col>
        <v-col
          v-else
          xl="8"
          sm="6"
          class="shrink"
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
              ref="next"
              :disabled="disableNext"
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
  mounted() {
    this.frElements = this.$el.getElementsByClassName("cds-free-response");

    this.updateFreeResponseList();
    this.updateDisableNext();

    this.frObserver = new MutationObserver((mutations) => {
      let needUpdate = false;
      mutations.forEach(mutation => {
        if (needUpdate) {
          return;
        }
        if (mutation.addedNodes.length > 0) {
          needUpdate = [...mutation.addedNodes].some(this.needUpdateNode);
        }
        if (!needUpdate && mutation.removedNodes.length > 0) {
          needUpdate = [...mutation.removedNodes].some(this.needUpdateNode);
        }
      });
      if (needUpdate) {
        this.updateFreeResponseList();
        this.updateDisableNext();
      }
    });
    this.frObserver.observe(this.$el, { childList: true, subtree: true });
  },
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
      type: Boolean
    },
    requireFr: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      frObserver: null,
      freeResponses: [],
      disableNext: false,
      frListener: null
    }
  },
  computed: {
    advance() {
      return !this.canAdvance;
    },
    header() {
      if (this.headerText instanceof Function) {
        return this.headerText(this.state);
      } else {
        return this.headerText;
      }
    }
  },
  methods: {

    // These methods are kinda hacky!
    // but they let us not ever have to deal with this stuff elsewhere
    // and not have to rewrite this in each guideline that has free responses
    updateFreeResponseList() {
      const frElements = this.$el.querySelectorAll(".cds-free-response");
      const frComponents = [...frElements].map(fr => fr.__vue__);
      for (let i = 0; i < frComponents.length; i++) {
        if (frComponents[i].$vnode.tag.indexOf("free-response") < 0) {
          frComponents[i] = frComponents[i].$parent;
        }
      }
      this.freeResponses = frComponents;

      if (this.freeResponses.length > 0 && this.frListener === null) {
        this.frListener = (_event) => {
          this.updateDisableNext();
        };
        this.$el.addEventListener('input', this.frListener);
      }
    },

    allFreeResponsesFilled() {
      return this.freeResponses.every(fr => fr.$refs.textarea.valid);
    },

    updateDisableNext() {
      this.disableNext = this.requireFr && !this.allFreeResponsesFilled();
    },

    needUpdateNode(node) {
      return node.classList != undefined &&
        (
          node.classList.contains("cds-free-response")
            ||
          node.querySelectorAll(".cds-free-response").length > 0
        );
    }
  }
};
</script>
