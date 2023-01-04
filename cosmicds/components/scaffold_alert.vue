<template>             
  <v-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
  >
    <v-row>
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
    <slot></slot>

    <v-divider
      class="my-4"
    >
    </v-divider>
    
    <v-row
      align="center"
      no-gutters
    >
      <v-col>
        <v-btn
          v-if="allowBack"  
          class="black--text"
          color="accent"
          elevation="2"
          @click="() => { $emit('back'); }"
        >
          back
        </v-btn>
        <span
          v-else
          style="font-size: 16px;"
        >
          <slot name="back-content"></slot>
        </span>
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
          style="font-size: 16px; border-left: solid 3px #FFD740; padding-left: 10px; color: #FFF8E1;"
        >
          <slot
            name="before-next"
          >
          </slot>
        </div>
      </v-col>
    </v-row>
  </v-alert>
</template>

<script>
module.exports = {
  props: {
    allowBack: {
      type: Boolean,
      default: true
    },
    headerText: {
      type: [String, Function],
      required: true
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
      return !this.canAdvance || this.canAdvance(this.state)
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
