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
    responseTag: String,
    rows: {
      type: Number,
      default: 1
    }
  },
  data: function () {
    return {
      response: "",
    };
  },

  created() {
    if (!this.responseTag) { return; }
    document.addEventListener("fr-initialize-response", this.onInitResponse)
  },

  methods: {
    dispatchEvent() {
      document.dispatchEvent(
        new CustomEvent("fr-update", {
          detail: {
            tag: this.responseTag,
            response: this.response
          }
        })
      );
    },

    onBlur(_event) {
      if (this.responseTag !== undefined) {
        this.dispatchEvent();
      }
    },

    onInitResponse(event) {
      const data = event.detail;
      if (data.gat !== this.responseTag) { return; }
      if (data.found) {
        this.response = data.response;
      }
      document.removeEventListener("fr-initialize-response", this.onInitResponse);
    }
  }
};
</script>
