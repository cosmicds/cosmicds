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
    }
  },
  data: function () {
    return {
      speechItems: [],
      speaking: false,
      
    };
  },
  mounted() {
    this.updateSpeechItems();
  },
  methods: {
    elementText(element) {
      return element.textContent;
    },
    updateSpeechItems() {
      const root = this.$parent.$el;
      const tagElements = this.tags.map(tag => [...root.getElementsByTagName(tag)]);
      const elements = [].concat(...tagElements);
      this.speechItems = elements.map(element => this.elementText(element));
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
      this.updateSpeechItems();
      const utterances = this.speechItems.map((item) => new SpeechSynthesisUtterance(item));
      utterances[utterances.length - 1].onend = (_event) => {
        this.speaking = false;
      }
      utterances.forEach((utterance) => synth.speak(utterance));
    }
  }
}
</script>
