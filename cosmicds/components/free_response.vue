<template>
  <v-textarea
    v-model="response"
    :outlined="outlined"
    :auto-grow="autoGrow"
    :filled="filled"
    :color="color"
    :rows="rows"
    :hint="hint"
    @blur="onBlur"
    v-intersect="dispatchInitializeEvent"
  >
    <template v-slot:label>
      <div>{{ label }}</div>
    </template>
  </v-textarea>
</template>

<script>
module.exports = {
  props: {
    autoGrow: Boolean,
    filled: Boolean,
    label: String,
    outlined: {
      type: Boolean,
      default: false
    },
    color: {
      type: String,
      default: "amber"
    },
    hint: {
      type: String,
      default: "Type your response here"
    },
    rows: {
      type: Number,
      default: 1
    },
    tag: String
  },
  data: function () {
    return {
      response: "",
      initialized: false,
    };
  },

  created() {
    if (!this.tag) { return; }
    document.addEventListener("fr-initialize-response", this.onInitResponse)
    this.dispatchInitializeEvent();
  },

  methods: {
    dispatchUpdateEvent() {
      document.dispatchEvent(
        new CustomEvent("fr-update", {
          detail: {
            tag: this.tag,
            response: this.response
          }
        })
      );
    },

    dispatchInitializeEvent() {
      if (!this.tag || this.initialized) { return; }
      document.dispatchEvent(
        new CustomEvent("fr-initialize", {
          detail: {
            tag: this.tag
          }
        })
      );
    },

    onBlur(_event) {
      if (this.tag !== undefined) {
        this.dispatchUpdateEvent();
      }
    },

    onInitResponse(event) {
      const data = event.detail;
      if (data.tag !== this.tag) { return; }
      if (data.found) {
        this.response = data.response;
      }
      this.initialized = true;
      document.removeEventListener("fr-initialize-response", this.onInitResponse);
    }
  }
};
</script>

<style scoped>
.v-input__slot {
  background-color: #FFAB4040!important;
}
</style>