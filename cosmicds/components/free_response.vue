<template>
  <v-textarea
    ref="textarea"
    v-model="response"
    :outlined="outlined"
    :auto-grow="autoGrow"
    :filled="filled"
    :color="color"
    :rows="rows"
    :hint="hint"
    :icon="icon"
    :rules="[isValid]"
    @blur="onBlur"
    v-intersect="dispatchInitializeEvent"
    class="cds-free-response"
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
    help: {
      type: String,
      default: "Invalid format"
    },
    hint: {
      type: String,
      required: false
    },
    icon: {
      type: String,
      required: false
    },
    rows: {
      type: Number,
      default: 1
    },
    rules: {
      type: Array, // Should be an array of functions with signature (string) => bool
      default: []
    },
    tag: String,
    type: {
      type: String,
      required: false
    }
  },
  data: function () {
    return {
      response: "",
      initialized: false,

      allowedInput: {
        int: {
          characters: "-01233456789",
          help: "Please input an integer"
        },
        uint: {
          characters: "0123456789",
          help: "Please input a non-negative integer"
        },
        float: {
          characters: "-0123456789",
          help: "Please input a number"
        }
      }
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
    },

    isValid(input) {
      if (this.type in this.allowedInput) {
        const inputData = this.allowedInput[this.type];
        const allowed = inputData.characters;
        const pattern = new RegExp(`^[${allowed}]+$`);
        return pattern.test(input) || inputData.help;
      }

      if (this.rules) {
        return this.rules.every(rule => rule(input)) || this.help;
      }

      return true;
    }
  }

};
</script>

<style scoped>
.v-input__slot {
  background-color: #FFAB4040!important;
}
</style>
