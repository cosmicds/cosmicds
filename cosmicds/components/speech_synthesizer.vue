<template>
  <v-icon
    v-if="speechItems.length > 0"
    @click="sayText"
  >
    mdi-voice
  </v-icon>
</template>

<script>
module.exports = {
  props: {
    tags: {
      type: Array,
      default: ['h1', 'h2', 'h3', 'p']
    }
  },
  data: function () {
    return {
      speechItems: []
    };
  },
  mounted() {
    const root = this.$parent.$el;
    const tagElements = this.tags.map(tag => [...root.getElementsByTagName(tag)]);
    const elements = [].concat(...tagElements);
    this.speechItems = elements.map(element => element.textContent.trim());
    if (this.headerText.length > 0) {
      this.speechItems.unshift(this.headerText);
    }
  },
  methods: {
    sayText() {
      const synth = window.speechSynthesis;
      if (synth.speaking) {
        synth.cancel();
      }

      // We say each speech item as its own utterance to try to get around this issue
      // https://bugs.chromium.org/p/chromium/issues/detail?id=679437
      //
      // It also has the nice benefit of giving a better pause between paragraphs
      for (const item of this.speechItems) {
        synth.speak(new SpeechSynthesisUtterance(item));
      }
    }
  }
}
</script>
