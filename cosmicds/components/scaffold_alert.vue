<template>             
  <v-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
  >
    <h3
      class="mb-4"
    >
      {{ headerText }}
    </h3>
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
          class="black--text"
          color="accent"
          elevation="2"
          @click="() => { $emit('back'); }"
        >
          back
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      <v-col
        v-if="advance"
        class="shrink"
      >
        <v-btn
          class="black--text"
          color="accent"
          elevation="2"
          @click="() => { $emit('next'); }"
        >
          next
        </v-btn>
      </v-col>
      <v-col
        v-else
        class="shrink"
      >
        <div
        >
          {{ nextText }}
        </div>
      </v-col>
    </v-row>
  </v-alert>
</template>

<script>
module.exports = {
  props: [
    "headerText",
    "nextText",
    "canAdvance",
    "state"
  ],
  data: function () {
    return {
    };
  },
  computed: {
    advance() {
      return !this.canAdvance || this.canAdvance(this.state)
    }
  }
};
</script>
