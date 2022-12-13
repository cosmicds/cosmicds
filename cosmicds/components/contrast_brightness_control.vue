<template>
  <v-card>
    <div class="sliders" v-if="enabled" :style="inlineStyle">
      <!-- Brighntess slider: a continuous (step="0") slider, logscale from .5, 1.5 -->
      <v-slider
        v-model="brightness"
        step="0"
        :min=0
        :max=4
        :label="parseFloat(brightness).toFixed(2)"
        hide-details=true
        style="margin:auto; width:75%"
        @change="update_style"
        >
        <!-- add tooltip to prepend slot -->
        <template v-slot:prepend>
          <v-tooltip left>
            <template v-slot:activator="{ on }">
              <v-icon 
                v-on="on"
                @click="resetBrightness"
                >
                  mdi-brightness-6
                </v-icon>
            </template>
            <span>Brightness<br>Press to reset</br></span>
          </v-tooltip>
        </template>
      </v-slider>
      <!-- Contrast: a continuous (step="0") slider, logscale from .5, 1.5 -->
      <v-slider
        v-model="contrast"
        step="0"
        :min="Math.log10(0.50)"  
        :max="Math.log10(1.50)"
        :label="Math.pow(10,contrast).toFixed(2)"
        hide-details=true
        style="margin:auto;width:75%;"
        @change="update_style"
        >
        <!-- add tooltip to prepend slot -->
        <template v-slot:prepend>
          <v-tooltip left>
            <template v-slot:activator="{ on }">
              <v-icon
                v-on="on"
                @click="resetContrast"
                >
                  mdi-contrast-circle
                </v-icon>
            </template>
            <span>Contrast<br>Press to reset</br></span>
          </v-tooltip>
        </template>
      </v-slider>
    </div>
  </v-card>

</template>



<style>


div.sliders {
}

</style>


<script>

module.exports = {

  // name of the component. used in the parent component
  // when importing as: import ContrastBrightnessControl from './path/to/ContrastBrightnessControl.vue'
  // ipyvuetify imports this as contrast-brightness-control
  name: 'ContrastBrightnessControl',

  // props: ['value'], // props are passed in from the parent. they should not be changed in the child
  props: {
    inlineStyle: {
      type: String,
      default: ""
    },
    enabled: {
      type: Boolean,
      default: true
    },
  },

  // data are local to the component. they can be changed
  //  data can be declared one of 3 ways:
  //  1. data() { return { key: value, ... } }
  //  2. data: function() { return { key: value, ... } }
  // 3. data: () => { return { key: value, ... } }
  data: () => {
    return {
      contrast: 0,
      brightness: 1,
    }
  },
  
  computed: {
    update_style() {
      // console.log('contrast', Math.pow(10, this.contrast) * 100)
      // console.log('brightness', this.brightness)
      // console.log('**************')
      let brightness = parseFloat(this.brightness).toFixed(2) * 100 // brightness in percent
      let contrast = Math.pow(10, this.contrast).toFixed(2) * 100  // contrast in percent
      let newstyle = { filter: `brightness(${brightness}%) contrast(${contrast}%)` }
      // sent this style to the parent. access using @newstyle="newstyle => { this.style = newstyle }"
      this.$emit('change_style',newstyle)
    },

    show() {
      console.log(this.enabled)
      return this.enabled
    }
  },
  

  methods: {
    resetContrast() {
      this.contrast = 0;
    },
    resetBrightness() {
      this.brightness = 1;
    },
  },
  
}

</script>
