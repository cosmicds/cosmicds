<template>
  <v-textarea
    v-model="response"
    :outlined="outlined"
    auto-grow
    filled
    :color="color"
    :rows="rows"
    :hint="hint"
    @blur="onBlur"
  >
    <template v-slot:label>
      <div>{{ questionLabel }}</div>
    </template>
  </v-textarea>
</template>

<script>
module.exports = {
  props: {
    questionLabel: String,
    outlined: {
      type: Boolean,
      default: false
    },
    color: {
      type: String,
      default: "deep-purple"
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
    };
  },

  created() {
    if (!this.tag) { return; }
    document.addEventListener("fr-initialize-response", this.onInitResponse)
  },

  methods: {
    dispatchEvent() {
      document.dispatchEvent(
        new CustomEvent("fr-update", {
          detail: {
            tag: this.tag,
            response: this.response
          }
        })
      );
    },

    onBlur(_event) {
      if (this.tag !== undefined) {
        this.dispatchEvent();
      }
    },

    onInitResponse(event) {
      const data = event.detail;
      if (data.tag !== this.tag) { return; }
      if (data.found) {
        this.response = data.response;
      }
      document.removeEventListener("fr-initialize-response", this.onInitResponse);
    }
  }
};
</script>
