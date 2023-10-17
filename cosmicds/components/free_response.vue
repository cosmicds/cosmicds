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
    helpMessage: {
      type: String,
      required: false
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
    allowEmpty: {
      type: Boolean,
      default: false
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
      defaultHelpMessage: "Invalid format",

      allowedInput: {
        int: {
          characters: "-01233456789",
          helpMessage: "Please input an integer"
        },
        uint: {
          characters: "0123456789",
          helpMessage: "Please input a non-negative integer"
        },
        float: {
          characters: "-0123456789.",
          helpMessage: "Please input a number"
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
      let valid = true;

      if (!this.allowEmpty && !input) {
        return "";
      }

      let helpMessage = this.helpMessage;
      if (this.type in this.allowedInput) {
        const inputData = this.allowedInput[this.type];
        const allowed = inputData.characters;
        const pattern = new RegExp(`^[${allowed}]+$`);

        valid = pattern.test(input);
        helpMessage = this.helpMessage || inputData.helpMessage;
      }
      helpMessage = helpMessage || this.defaultHelpMessage;

      if (this.rules.length > 0) {
        valid = this.rules.every(rule => rule(input));
      }

      return valid || helpMessage;
    }
  }

};
</script>

<style scoped>
.v-input__slot {
  background-color: #FFAB4040!important;
}
</style>
