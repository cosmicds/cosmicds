<template>
  <v-card min-width="300">
    <v-list>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Speech Reader</v-list-item-title>
          <v-list-item-subtitle>Adjust speech settings</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item>
        <v-switch
          v-model="autoread"
          label="Automatically read text"
        ></v-switch>
      </v-list-item>
      <v-list-item>
        <v-slider
          v-model="rate"
          :label="rate.toFixed(1)"
          color="blue"
          :min="0.5"
          :max="2"
          :step="0.1"
          :thumb-label="false"
        >
        <template v-slot:prepend>
          <v-tooltip left>
            <template v-slot:activator="{ on }">
              <v-icon
                v-on="on"
                @click="rate = 1"
              >
                mdi-speedometer
              </v-icon>
            </template>
            Reset rate
          </v-tooltip>
        </template>
        </v-slider>
      </v-list-item>
      <v-list-item>
        <v-slider
          v-model="pitch"
          :label="pitch.toFixed(1)"
          color="blue"
          :min="0.1"
          :max="2"
          :step="0.1"
          :thumb-label="false"
        >
        <template v-slot:prepend>
          <v-tooltip left>
            <template v-slot:activator="{ on }">
              <v-icon
                v-on="on"
                @click="pitch = 1"
              >
                mdi-music-note
              </v-icon>
            </template>
            Reset pitch
          </v-tooltip>
        </template>
        </v-slider>
      </v-list-item>
      <v-list-item>
        <v-select
          v-model="voice"
          :items="voices"
          :item-text="voice => `${voice.name} (${voice.lang})`"
          item-value="name"
          label="Select voice"
        ></v-select>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
module.exports = {
  created() {
    window.speechSynthesis.onvoiceschanged = (_event) => {
      this.updateVoiceList();
    };
    this.updateVoiceList();

    this.updateAttributes(this.initialState);
  },
  data() {
    return {
      autoread: false,
      pitch: 1,
      rate: 1,
      voiceURIs: [
        'Google US English',
        'urn:moz-tts:speechd:English%20(America)?en',
        'Alex',
        'Tessa',
        'urn:moz-tts:osx:com.apple.speech.synthesis.voice.Alex',
        'urn:moz-tts:osx:com.apple.speech.synthesis.voice.tessa',
        'com.apple.speech.synthesis.voice.Alex',
        'com.apple.speech.synthesis.voice.tessa',
        'Microsoft Zira - English (United States)',
        'Microsoft Aria Online (Natural) - English (United States)',
        'urn:moz-tts:sapi:Microsoft Zira - English (United States)?en-US'
      ],
      voices: [],
      voice: null
    }
  },
  methods: {
    updateVoiceList() {
      this.voices = window.speechSynthesis.getVoices().filter(voice => this.voiceURIs.includes(voice.voiceURI));
    },
    updateAttributes(state) {
      this.autoread = state?.autoread ?? false;
      this.pitch = state?.pitch ?? 1;
      this.rate = state?.rate ?? 1;
    },
  },
  watch: {
    autoread(read) {
      this.autoread_changed(read);
    },
    pitch(value) {
      this.pitch_changed(value);
    },
    rate(value) {
      this.rate_changed(value);
    },
    voice(newVoice) {
      this.voice_changed(newVoice.voiceURI);
    },
    initialState(state) {
      this.updateAttributes(state);
    }
  }
}
</script>
