<template>
  <span>
    <slot>
      <v-btn
        icon
      >
        <v-icon
          @click="(_event) => speak()"
        >
          {{ speaking ? 'mdi-stop' : 'mdi-voice' }}
        </v-icon>
      </v-btn>
    </slot>
  </span>
</template>

<script>
module.exports = {
  props: {
    selectors: {
      type: Array,
      default: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', ':not(mjx-assistive-mml) > mjx-container']
    },
    stopOnClose: {
      type: Boolean,
      default: true
    },
    root: {
      type: [Object, Function],
      default: null
    },
    elementFilter: {
      type: [Function],
      default: null
    },
    autospeakOnChange: {
      type: [Boolean, Number],
      default: null
    },
    speakFlag: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      utteranceSpeaking: false,
      speakingTimeoutID: null,
      intervalID: 0,
      rootElement: null,
      iconNameMap: {
        'cached': 'reset'
      },
      defaultVoicesURIs: [
        "Microsoft Aria Online (Natural) - English (United States)",
        "Google US English",
        "com.apple.speech.synthesis.voice.tessa"
      ],
      defaultVoice: null,
      utterances: new Set(),
      findingRoot: false
    };
  },
  mounted() {
    this.intersectionCallback = (entries, _observer) => {

      // The IntersectionObserver is called once as soon as it's instantiated
      // We don't want that!
      // so here's a workaround
      // This is set in the rootElement watcher, where the observer is created
      // if (this.findingRoot) {
      //   this.findingRoot = false;
      //   return;
      // }

      entries.forEach((entry) => {
        if (entry.target !== this.rootElement) { return; }
        if (!entry.isIntersecting) {
          this.stopThisSpeaking();
        } else if (!this.speaking && entry.isIntersecting && this.getSpeechOptions().autoread > 0) {
          this.triggerAutospeak(true);
        }
      });
    };
    this.$nextTick(() => {
      this.findRootElement();
    });
  },
  destroyed() {
    if (this.stopOnClose && this.isSpeaking()) {
      clearInterval(this.intervalID);
      this.speaking = false;
      window.speechSynthesis.cancel();
    }
  },
  computed: {
    speaking: {
      get() {
        return this.utteranceSpeaking;
      },
      set(value) {
        if (this.speakingTimeoutID) {
          clearTimeout(this.speakingTimeoutID);
        }
        this.speakingTimeoutID = setTimeout(() => {
          this.utteranceSpeaking = value;
        }, 300);
      }
    }
  },
  methods: {

    triggerAutospeak(forceSpeak=true) {
      const appComponent = this.$root.$children[0].$children[0];
      // const appComponent = document.querySelector("#inspire").__vue__;
      if (appComponent.app_state.speech_autoread) {
        this.$nextTick(() => this.speak(forceSpeak));
      }
    },

    elementText(element) {

      // Replace any MDI icons with text representing their name
      const clone = element.cloneNode(true);
      const mdiPrefix = "mdi-";
      const icons = clone.querySelectorAll(`[class*='${mdiPrefix}']`);
      icons.forEach(icon => {
        const classes = [...icon.classList].filter(cls => cls.startsWith(mdiPrefix));
        if (classes.length === 0) {
          icon.remove();
        } else {
          const txt = document.createElement("text");
          const cls = classes[0];
          let iconName = cls.slice(mdiPrefix.length);
          txt.textContent = this.iconNameMap[iconName] ?? iconName.replace("-", " ");
          icon.parentNode?.replaceChild(txt, icon);
        }
      });

      // Replace any MathJax with its semantic speech text
      if (clone.tagName === "mjx-container") {
        const speechText = clone.getAttribute("aria-label");
        if (speechText) {
          const txt = document.createElement("text");
          txt.textContent = speechText;
          clone.parentNode?.replaceChild(txt, clone);
        } else {
          clone.remove();
        }
      }

      return clone.textContent.trim();

    },
    makeUtterance(text, options) {
      const utterance = new SpeechSynthesisUtterance(text);

      options = options || this.getSpeechOptions();
      Object.keys(options).forEach(key => {
        utterance[key] = options[key];
      });
      transformRate(utterance);

      // The interval is to work around this issue:
      // https://bugs.chromium.org/p/chromium/issues/detail?id=679437
      //
      // We could just use one interval for the entire block of text items
      // but the pause-resume is sometimes slightly audible, so better to minimize that.
      // Note that the pause-resume won't happen if the text takes longer than 14 seconds to say
      const synth = window.speechSynthesis;
      utterance.onstart = (_event) => {
        this.intervalID = setInterval(() => {
          synth.pause();
          synth.resume();
        }, 14000);
        synth.utterance = utterance;
        this.speaking = true;
      }
      utterance.onend = (_event) => {
        synth.utterance = null;
        this.speaking = false;
        this.utterances.delete(utterance);
        clearInterval(this.intervalID);
      }

      return utterance;
    },
    findRootElement() {
      if (this.root instanceof Element) {
        this.rootElement = this.root;
      } else if (this.root instanceof Function) {
        this.rootElement = this.root();
      } else {
        this.rootElement = this.$parent.$el;
      }
    },
    getSpeechOptions() {
      // TODO: Find a better way to access this piece of global state!
      const appComponent = this.$root.$children[0].$children[0];
      // const appComponent = document.querySelector("#inspire").__vue__;
      const state = appComponent.app_state;
      const voiceName = state.speech_voice;
      this.defaultVoice = this.defaultVoice || window.speechSynthesis.getVoices().find(voice => this.defaultVoicesURIs.includes(voice.voiceURI));
      const voice = window.speechSynthesis.getVoices().find(voice => voice.name == voiceName) || this.defaultVoice;
      const options = {
        autoread: state.speech_autoread ?? false,
        pitch: state.speech_pitch ?? 1,
        rate: state.speech_rate ?? 1,
      };
      if (voice) {
        options.voice = voice;
      }
      return options;
    },
    // Taken from https://www.geeksforgeeks.org/how-to-check-if-an-element-is-visible-in-dom/
    // TODO: Is there a better way to check?
    //
    // Note that element.checkVisibility() doesn't work on Safari:
    // https://caniuse.com/mdn-api_element_checkvisibility
    isElementVisible(element) {
      if (element.checkVisibility) {
        return element.checkVisibility();
      }
      return element.offsetWidth || 
             element.offsetHeight || 
             element.getClientRects().length;
    },
    getSpeechItems(selectors=this.selectors) {
      if (this.rootElement === null) {
        this.findRootElement();
      }
      const selectedElements = this.rootElement.querySelectorAll(selectors.join(","));
      let elements = [].concat(...selectedElements).filter(this.isElementVisible);
      if (this.elementFilter) {
        elements = elements.filter(this.elementFilter);
      }
      const items = elements.map(element => this.elementText(element)).filter(text => text.length > 0);
      return items;
    },

    speakForSelectors(selectors) {
      this.speak(true, selectors)
    },

    speak(forceSpeak=false, selectors=this.selectors) {
      const wasSpeaking = this.isSpeaking();
      this.cancelSpeech();
      if (wasSpeaking && !forceSpeak) {
        return;
      }

      // We say each speech item as its own utterance
      // This gives a nice pause between paragraphs
      this.speaking = true;
      const items = this.getSpeechItems(selectors);
      const options = this.getSpeechOptions();
      const utterances = items.map(item => this.makeUtterance(item, options));
      this.utterances = new Set(utterances);

      // const lastUtterance = utterances[utterances.length - 1];
      // const lastOnEnd = lastUtterance.onend;
      // lastUtterance.onend = (event) => {
      //   lastOnEnd(event);
      //   this.speaking = false;
      // }
      
      //utterances.forEach((utterance) => synth.speak(utterance));
      utterances.forEach(utterance => {
        window.speechSynthesis.speak(utterance);
      });
    },

    stopThisSpeaking() {
      this.speaking = false;
      if (this.isSpeaking()) {
        this.cancelSpeech();
      }
    },

    cancelSpeech() {
      window.speechSynthesis.utterance = null;
      window.speechSynthesis.cancel();
      this.utterances.clear();
      clearInterval(this.intervalID);
      this.speaking = false;
    },

    // I made this a method rather than a computed since synth.speaking is not reactive
    isSpeaking() {
      const synth = window.speechSynthesis;
      return synth.speaking && this.utterances.has(synth.utterance);
    },

    function detectBrowser() {
      let userAgent = navigator.userAgent;
      let browserName;

      if (userAgent.match(/chrome|chromium|crios/i)) {
        browserName = "chrome";
      } else if (userAgent.match(/firefox|fxios/i)) {
        browserName = "firefox";
      } else if (userAgent.match(/safari/i)) {
        browserName = "safari";
      } else if (userAgent.match(/opr\//i)) {
        browserName = "opera";
      } else if (userAgent.match(/edg/i)) {
        browserName = "edge";
      } else {
        browserName = null;
      }

      return browserName
    },

    transformRate(utterance) {
      const uri = utterance.voice.voiceURI;
      if (uri === "Google US English") {
        utterance.rate = Math.sqrt(2 * utterance.rate);
      } else if (uri === 'Microsoft Zira - English (United States)') {
        const browser = this.detectBrowser();
        if (browser === 'chrome') {
          utterance.rate = Math.pow(utterance.rate, 2.5);
        } else if (browser === 'edge') {
          utterance.rate = 1.5 * utterance.rate;
        } else if (browser === 'firefox') {
          utterance.rate = 1.2 * utterance.rate;
        }
      }
    },

  watch: {
    // For the v-dialog slideshows, using nextTick (again, since triggerAutospeak uses it)
    // didn't seem to be enough - the DOM changes hadn't finished propagating yet.
    // But this does the trick, and I don't notice it at all
    autospeakOnChange(_item) {
      setTimeout(() => {{
        this.triggerAutospeak();
      }}, 100);
    },

    speakFlag(flag) {
      if (flag) {
        setTimeout(() => {{
          this.triggerAutospeak();
        }}, 100);
      } else {
        if (this.isSpeaking()) {
          window.speechSynthesis.cancel();
          this.speaking = false;
        }
      }
    },
    rootElement(newRoot, oldRoot) {
      this.findingRoot = true;
      if (this.intersectionObserver) {
        this.intersectionObserver.unobserve(oldRoot);
      }
      this.intersectionObserver = new IntersectionObserver(this.intersectionCallback);
      this.intersectionObserver.observe(newRoot);
    }
  }
}
</script>
