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
    class="cds-free-response"
  >
    <template v-slot:label>
      <div>{{ label }}</div>
    </template>
  </v-textarea>
</template>

<script>
module.exports = {
  
  name: "FreeResponse",
  
  props: {
    initialResponse: {
      type: String,
      required: false,
      default: undefined
    },
    initialized: {
      type: Boolean,
      default: false
    },
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
      type: Number | String,
      default: 1
    },
    allowEmpty: {
      type: Boolean,
      default: false
    },
    rules: {
      type: Array, // Should be an array of functions with signature (string) => bool
      default: () => []
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
      defaultHelpMessage: "Invalid format",

      allowedInput: {
        int: {
          characters: "-01233456789",
          helpMessage: "Please input an integer. (Be sure there are no spaces.)"
        },
        uint: {
          characters: "0123456789",
          helpMessage: "Please input a non-negative integer. (Be sure there are no spaces.)"
        },
        float: {
          characters: "-0123456789.",
          helpMessage: "Please input a number. (Be sure there are no spaces.)"
        }
      }
    };
  },

  created() {
    if (!this.tag) { return; }
    // console.log("FreeResponse created", this.tag);
    // console.log("FreeResponse initiallized", this.initialized);
    // console.log("FreeResponse initialResponse", this.initialResponse, typeof this.initialResponse);
    this.dispatchInitializeEvent();
    this.response = this.initialResponse;
  },
  
  
  emits: {
    "fr-initialize": function (event) {
      return typeof event.tag === "string";
    },
    "fr-update": function (event) {
      return typeof event.tag === "string" && typeof event.response === "string";
    },
  },

  methods: {
    dispatchEvent(eventType, detail) {
      console.log("dispatching event", eventType, detail);
      this.$emit(eventType, detail);
    },
    
    dispatchUpdateEvent() {
      this.dispatchEvent("fr-update", {
        tag: this.tag,
        response: this.response
      });
    },

    dispatchInitializeEvent() {
      if (!this.tag || this.initialized) { return; }
      this.dispatchEvent("fr-initialize", {
        tag: this.tag
      }
      );
    },

    onBlur(_event) {
      if (this.tag !== undefined) {
        this.dispatchUpdateEvent();
      }
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
  },
  

}
</script>

<style scoped>
.v-input__slot {
  background-color: #FFAB4040!important;
}
</style>
