<template>
  <v-icon
    @click="sayText"
  >
    {{ speaking ? 'mdi-stop' : 'mdi-voice' }}
  </v-icon>
</template>

<script>
module.exports = {
  props: {
    tags: {
      type: Array,
      default: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']
    },
    stopOnClose: {
      type: Boolean,
      default: true
    }
  },
  data: function () {
    return {
      speaking: false,
    };
  },
  destroyed() {
    if (this.stopOnClose && this.speaking) {
      window.speechSynthesis.cancel();
    }
  },
  methods: {
    elementText(element) {
      return element.textContent;
    },
    getSpeechItems() {
      const root = this.$parent.$el;
      const tagElements = this.tags.map(tag => [...root.getElementsByTagName(tag)]);
      const elements = [].concat(...tagElements);
      const items = elements.map(element => this.elementText(element));
      return items;
    },
    sayText() {
      const synth = window.speechSynthesis;
      if (synth.speaking) {
        synth.cancel();
        this.speaking = false;
        return;
      }

      // We say each speech item as its own utterance to try to get around this issue:
      // https://bugs.chromium.org/p/chromium/issues/detail?id=679437
      //
      // It also has the nice benefit of giving a better pause between paragraphs
      this.speaking = true;
      const items = this.getSpeechItems();
      const utterances = items.map((item) => new SpeechSynthesisUtterance(item));
      utterances[utterances.length - 1].onend = (_event) => {
        this.speaking = false;
      }
      utterances.forEach((utterance) => synth.speak(utterance));
    }
  }
}
</script>
