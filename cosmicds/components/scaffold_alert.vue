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
          {{ headerText }}
        </h3>
      </v-col>
      <v-col
        cols="2"
      >
        <speech-synthesizer />
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
      <v-col
        cols="6"
      >
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
        cols="6"
        class="shrink text-right"
      >
        <v-btn
          v-if="advance"
          class="black--text"
          color="accent"
          elevation="2"
          @click="() => { $emit('next'); }"
        >
          next
        </v-btn>
        <span
          v-else
          style="font-size: 16px;"
        >
          <slot name="next-content"></slot>
        </span>
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
      type: String,
      required: true
    },
    backContent: {
      type: String
    },
    nextContent: {
      type: String
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
    }
  }
};
</script>
