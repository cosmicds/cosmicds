<template>
  <v-app id="inspire">
    <v-overlay :value="!hub_user_loaded"
      opacity="0.75"
      z-index=1000>
      <v-progress-circular
      indeterminate
      color="primary"
      ></v-progress-circular>
      Loading User Data...
    </v-overlay>
    <v-app-bar
      app
      color="primary"
      dark
      src="https://www.astropix.org/archive/esahubble/heic1518b/esahubble_heic1518b_1600.jpg"
      clipped-right
      flat
      height="72"
      style="z-index: 50;"
    >
      <template v-slot:img="{ props }">
        <v-img
          v-bind="props"
          gradient="to top right, rgba(25, 71, 161, .2), rgba(8, 47, 104, .9)"
        ></v-img>
      </template>

      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title class="mr-5">
        <h2>{{ story_state.title }}</h2>
      </v-toolbar-title>

      <v-toolbar-title>Cosmic Data Stories</v-toolbar-title>

      <v-spacer></v-spacer>
      <v-tooltip
        bottom
      >
        <template
          v-slot:activator="{ on, attrs }"
        >
          <v-menu
            v-model="speech_menu"
            :close-on-content-click="false"
            offset-y
          >
            <template v-slot:activator="{ props }">
              <v-btn
                icon
                v-bind:value="[props, attrs]"
                v-on="on"
                @click="speech_menu = !speech_menu"
              >
                <v-icon>mdi-voice</v-icon>
              </v-btn>
            </template>
            <speech-settings
              :state="app_state"
            />
          </v-menu>
        </template>
        Adjust speech settings
      </v-tooltip>
      <v-tooltip
        bottom
      >
        <template
          v-slot:activator="{ on, attrs }"
        >
          <v-btn
            icon
            v-bind="attrs"
            v-on="on"
            @click="
              app_state.dark_mode = !app_state.dark_mode
            "
          >
            <v-icon>mdi-brightness-4</v-icon>
          </v-btn>
        </template>
        {{ app_state.dark_mode ? 'switch to light mode' : 'switch to dark mode' }}
      </v-tooltip>
      <v-chip
        v-if="story_state.has_scoring"
        color="green"
        outlined
        class="mx-2"
        style="background-color:#000A!important;"
      >
        <span
          class="white--text mr-2"
        >
          <strong>{{ `${story_state.total_score} ${story_state.total_score == 1 ? 'point' : 'points'}` }}</strong>
        </span>
        <v-icon
          color="green"
        >
          mdi-piggy-bank
        </v-icon>

      </v-chip>

      <v-responsive
        v-if="false"
        max-width="156"
        class="mx-4"
      >
        <v-text-field
          dense
          flat
          hide-details
          rounded
          solo-inverted
        ></v-text-field>
      </v-responsive>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app width="300">
      <!-- TODO: This should be a built-in prop, but border radius requires explicit style def... -->
      <v-sheet height="72" width="100%" style="border-radius: 0px">
        <v-list class="ma-0 pa-0">
          <v-list-item>
            <v-list-item-action
              class="mr-3"
            >
              <v-avatar
                color="warning"
              >
                <v-icon dark>mdi-account-circle</v-icon>
              </v-avatar>
            </v-list-item-action>

            <v-list-item-content>
              <v-list-item-title>
                Guest Student {{ student_id }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-sheet>

      <!-- List of stages for this story -->
      <v-stepper
        v-model="story_state.stage_index"
        vertical
        flat
        non-linear
        class="elevation-0"
        @change="story_state.step_index = story_state.stages[story_state.stage_index].step_index"
      >
        <template v-for="(stage, key, index) in story_state.stages">
          <v-stepper-step
            :key="index"
            :editable="app_state.allow_advancing || index == 0 || story_state.max_stage_index >= index"
            :complete="story_state.max_stage_index > index"
            :step="index"
            :edit-icon="'$complete'"
          >
            {{ stage.title }}
          </v-stepper-step>

          <v-stepper-content :key="index" :step="index" class="my-0 py-0">
            <!-- Section containing each stage's individual steps -->
            <v-list dense nav>
              <v-list-item-group
                v-model="story_state.step_index"
                color="info"
              >
                <v-list-item
                  v-for="(step, i) in story_state.stages[key].steps"
                  :key="i"
                  :disabled="i > 0 && !story_state.stages[key].steps[i-1].completed"
                >
                  <v-list-item-action>
                    <template v-if="step.completed">
                      <v-icon>mdi-checkbox-marked-circle</v-icon>
                    </template>
                    <template v-else>
                      <v-icon>mdi-checkbox-blank-circle-outline</v-icon>
                    </template>
                  </v-list-item-action>

                  <v-list-item-content>
                    <v-list-item-title>{{ step.title }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-stepper-content>
        </template>
      </v-stepper>
    </v-navigation-drawer>

    <!--
    <v-navigation-drawer
        app
        clipped
        right
        permanent
        expand-on-hover
    >
      <v-list
          nav
          dense
      >
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-folder</v-icon>
          </v-list-item-icon>
          <v-list-item-title>My Files</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Shared with me</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-star</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Starred</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    -->
    
    <v-main>
      <v-content>
        <v-container fluid>
          <v-tabs-items v-model="story_state.stage_index">
            <v-tab-item
              v-for="(stage, key, index) in story_state.stages"
              :key="index"
            >
              <v-card flat>
                <v-card-title style="display: none;">{{ stage.title }}</v-card-title>
                <jupyter-widget :widget="stage.model_id"/>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-container>
      </v-content>
    </v-main>

    <v-footer
      app
      padless
      inset
      style="z-index: 50;"
      dark
      color="primary darken-1"
    >
      <v-row justify="center" no-gutters>
        <v-col
          class="py-2 text-center"
          cols="3"
        >          
          {{ new Date().getFullYear() }} — <strong>CosmicDS</strong>

          <img class="icon-img" alt="CosmicDS Logo" src="https://raw.githubusercontent.com/cosmicds/minids/main/assets/cosmicds_logo_for_dark_backgrounds.png"
              />

          <img class="icon-img" alt="SciAct Logo" src="https://raw.githubusercontent.com/cosmicds/minids/main/assets/NASA_Partner_color_300_no_outline.png"
            />
        </v-col>
        <v-col
          class="text-left"
          cols="9"
        >
          <span style="color:#BDBDBD!important; font-size:90%; line-height:80%; align-items:center">The material contained on this website is based upon work supported by NASA under award No. 80NSSC21M0002. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Aeronautics and Space Administration.</span>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  created() {
    // NOTE: THIS IS ONLY VALID FOR CONTAINDS USAGE
    // The environment does not always reflect the actual user account that's
    // using the app, so fetch the current user info
    var vm = this;

    fetch(
        '/hub/dashboards-api/hub-info/user',
        {
            mode: 'no-cors',
            credentials: 'same-origin',
            headers: new Headers({'Access-Control-Allow-Origin':'*'})
        }
    ).then(response=>response.json())
    .then(data=>{
        console.log(data);
        vm.hub_user_info = data;
    });
  },
  async mounted() {

    // We ultimately don't want to expose this
    // It's just for testing purposes
    window.cdsApp = this;

    const app = this;
    if (!window.customElements.get("cds-input")) {

      class CustomInput extends HTMLElement {

        static app = app;

        constructor() {
          super();
          this.attachShadow({mode: "open"});
          this.input = document.createElement("input");
          this.input.style.width = "50px";
          this.input.onchange = this.handleChangeEvent.bind(this);
          this.shadowRoot.append(this.input);

          // For inputs that aren't created when the story is initialized
          // (i.e. in a MathJax intersection observer)
          // we need this to correctly initialize the value
          const tag = this.getAttribute("tag");
          if (tag) {
            const application = CustomInput.app;
            if (tag in application.story_state.inputs) {
              this.input.value = application.story_state.inputs[tag];
            }
          }
        }

        handleChangeEvent(event) {
          const element = event.target;
          const text = element.value;
          this.onUpdateText(text);
        }

        set value(text) {
          this.input.value = text;
        }

        get value() {
          return this.input.value;
        }

        onUpdateText(text) {
          const tag = this.getAttribute("tag");
          if (!tag) { return; }
          const application = CustomInput.app;
          application.story_state.inputs[tag] = text;
          // AFAICT, we need to call this here to update the state Python-side
          app.update_state();
        }
      }

      window.customElements.define("cds-input", CustomInput);
    } else {
      const inputClass = window.customElements.get("cds-input");
      inputClass.app = app;
    }

    // Check whether or not we're using voila
    // Based on the approach used here: https://github.com/widgetti/ipyvuetify/blob/master/js/src/jupyterEnvironment.js
    const item = []
      .slice
      .call(document.getElementsByTagName('script'))
      .map(e => e.src)
      .find(e => e.includes('voila/static'));
    this.app_state.using_voila = item !== undefined;

    // Colors that seem to work consistently are in Section "4.3. Colors via svgnames option," pg 42 of this doc: https://ctan.math.washington.edu/tex-archive/macros/latex/contrib/xcolor/xcolor.pdf
    window.MathJax = {
      loader: {load: ['[tex]/color', '[tex]/bbox', 'a11y/semantic-enrich']},
      tex: {
        packages: {'[+]': ['input', 'color', 'bbox']},
        color: {
          padding: '4px'
        }
      },
      startup: {
        ready() {
          const Configuration = MathJax._.input.tex.Configuration.Configuration;
          const CommandMap = MathJax._.input.tex.SymbolMap.CommandMap;
          const TEXCLASS = MathJax._.core.MmlTree.MmlNode.TEXCLASS;
          
          new CommandMap('input', {input: 'Input'}, {
            Input(parser, name) {
              const xml = parser.create('node', 'XML');
              const id = parser.GetBrackets(name, '');
              const cls = parser.GetBrackets(name, '');
              const tag = parser.GetBrackets(name, '');
              const value = parser.GetArgument(name);
              const elementData = {
                id: id, class: cls, tag: tag, value: value,
                xmlns: 'http://www.w3.org/1999/xhtml'
              };
              xml.setXML(MathJax.startup.adaptor.node('cds-input', elementData), MathJax.startup.adaptor);
              xml.getSerializedXML = function () {
                return this.adaptor.outerHTML(this.xml) + '</cds-input>';
              }
              parser.Push(
                parser.create('node', 'TeXAtom', [
                  parser.create('node', 'semantics', [
                    parser.create('node', 'annotation-xml', [
                      xml
                    ], {encoding: 'application/xhtml+xml'})
                  ])
                ], {texClass: TEXCLASS.ORD})
              );
            }
          });
          Configuration.create('input', {handler: {macro: ['input']}});

          MathJax.startup.defaultReady();
        }
      },
      options: {
        menuOptions: {
          settings: {
            assistiveMml: true,
            inTabOrder: false
          }
        },
        a11y: {
          speech: true,
          sre: {
            speech: 'deep'
          }
        }
      }
    };

    // Grab MathJax itself
    // We want to wait for it to finish loading, in case there are
    // any elements that need to be typeset on the initial screen
    await new Promise((resolve, reject) => {
      const mathJaxScript = document.createElement('script');
      mathJaxScript.async = false;
      mathJaxScript.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js";
      document.head.appendChild(mathJaxScript);
      mathJaxScript.onload = (_e) => resolve();
      mathJaxScript.onerror = (_e) => reject();
    });
    await MathJax.startup.promise;

    // Not all of our elements are initially in the DOM,
    // so we need to account for that in order to get MathJax
    // to render their formulae properly
    const mathJaxOpeningDelimiters = [ "$$", "\\(", "\\[" ];
    const containsMathJax = node => mathJaxOpeningDelimiters.some(delim => node.innerHTML.includes(delim));
    const elementToScan = node => node.nodeType === Node.ELEMENT_NODE;
    const mathJaxCallback = function(mutationList, _observer) {
      mutationList.forEach(mutation => {
        if (mutation.type === 'childList') {

          const needTypesetting = [];
          mutation.addedNodes.forEach(node => {
            if (elementToScan(node) && containsMathJax(node)) {
              needTypesetting.push(node);
            }
          });
          if (needTypesetting.length > 0) {
            MathJax.typesetPromise(needTypesetting);
          }

          const toClear = [];
          mutation.removedNodes.forEach(node => {
            if (elementToScan(node) && containsMathJax(node)) {
              toClear.push(node);
            }
          })
          if (toClear.length > 0) {
            MathJax.typesetClear(toClear);
          }
        }
      });
    }
    const observer = new MutationObserver(mathJaxCallback);
    const options = { childList: true, subtree: true };
    observer.observe(this.$el, options);

    // Make dialogs draggable
    // This is a modified version of the code from https://github.com/vuetifyjs/vuetify/issues/4058#issuecomment-450636420
    // In particular, the reliance on setInterval has been removed in favor of a ResizeObserver
    const d = {};
    const titleClasses = ["v-card__title", "v-toolbar__content"];
    document.addEventListener("mousedown", e => {
      const classes = Array.from(e.target.classList);
      const containsTitleClass = classes.some(x => titleClasses.includes(x));
      if (!containsTitleClass) return;
      const closestDialog = e.target.closest(".v-dialog.v-dialog--active");
      if (e.button === 0 && closestDialog != null) { // element which can be used to move element
        const boundingRect = closestDialog.getBoundingClientRect();
        d.el = closestDialog; // element which should be moved
        d.title = e.target;
        d.mouseStartX = e.clientX;
        d.mouseStartY = e.clientY;
        d.elStartX = boundingRect.left;
        d.elStartY = boundingRect.top;
        d.el.style.position = "fixed";
        d.el.style.margin = 0;
        d.oldTransition = d.el.style.transition;
        d.el.style.transition = "none";
        d.title.classList.add("dragging");
        d.overlays = document.querySelectorAll(".v-overlay.v-overlay--active");
        d.overlays.forEach(overlay => overlay.style.display = "none");
      }
    });
    document.addEventListener("mousemove", e => {
        if (d.el === undefined) return;
        const boundingRect = d.el.getBoundingClientRect();
        d.el.style.left = Math.min(
            Math.max(d.elStartX + e.clientX - d.mouseStartX, 0),
            window.innerWidth - boundingRect.width
        ) + "px";
        d.el.style.top = Math.min(
            Math.max(d.elStartY + e.clientY - d.mouseStartY, 0),
            window.innerHeight - boundingRect.height
        ) + "px";
    });
    document.addEventListener("mouseup", () => {
        if (d.el === undefined) return;
        d.el.style.transition = d.oldTransition;
        d.el = undefined;
        d.title.classList.remove("dragging");
        d.overlays.forEach(overlay => overlay.style.display = '');
    });

    // If the window changes size, the dialog may be partially/completely out of bounds
    // We fix that here
    const resizeObserver = new ResizeObserver(entries => {
      entries.forEach(entry => {
        const dialogs = entry.target.querySelectorAll(".v-dialog.v-dialog--active");
        dialogs.forEach(dialog => {
          const boundingRect = dialog.getBoundingClientRect();
          dialog.style.left = Math.min(parseInt(dialog.style.left), window.innerWidth - boundingRect.width) + "px";
          dialog.style.top = Math.min(parseInt(dialog.style.top), window.innerHeight - boundingRect.height) + "px";
        });
      });
    });
    resizeObserver.observe(document.body);
    //this.onLoadStoryState(this.story_state);

    document.addEventListener("mc-score", (e) => {
      app.update_mc_score(e.detail);
      app.update_state();
    });

    document.addEventListener("fr-update", (e) => {
      app.update_free_response(e.detail);
      app.update_state();
    });

    document.addEventListener("mc-initialize", this.handleMCInitialization);
    document.addEventListener("fr-initialize", this.handleFRInitialization);
  },
  methods: {
    getCurrentStage: function () {
      return this.$data.story_state.stages[this.$data.story_state.stage_index];
    },
    onLoadStoryState: function(state) {
      if (state.inputs === undefined) return;
      for (const [key, value] of Object.entries(state.inputs)) {
        const els = document.querySelectorAll(`[tag=${key}]`);
        els.forEach(el => { el.value = String(value); });
      }
    },
    handleFRInitialization: function(event) {
      const tag = event.detail.tag;
      for (const values of Object.values(this.story_state.responses)) {
        if (tag in values) {
          const response = values[tag];
          document.dispatchEvent(
            new CustomEvent("fr-initialize-response", {
              detail: {
                response: response,
                tag: tag,
                found: true,
              }
            })
          )
        }
      }

      // If we don't have any data for this FR
      document.dispatchEvent(
          new CustomEvent("fr-initialize-response", {
            detail: {
              tag: tag,
              found: false,
            }
          })
      );
    },
    handleMCInitialization: function(event) {
      const tag = event.detail.tag;
      for (const values of Object.values(this.story_state.mc_scoring)) {
        if (tag in values) {
          const data = values[tag];
          document.dispatchEvent(
            new CustomEvent("mc-initialize-response", {
              detail: {
                ...data,
                found: true,
                tag: tag
              }
            })
          );
          return;
        }
      }
      // If there isn't a score for this MC, let it know
      document.dispatchEvent(
          new CustomEvent("mc-initialize-response", {
            detail: {
              found: false,
              tag: tag
            }
          })
      );
    }
  }
};
</script>

<style id="cosmicds-app">
html,
body {
  margin: 0;
  padding: 0;
}

td:first-child, th:first-child {
  min-width: 180px!important;
}

td.text-start {
  padding: 8px 16px!important;
}

.v-navigation-drawer .v-list-item--active.theme--light .v-list-item__content {
  color: black;
  z-index: 1;
}

.v-navigation-drawer .v-list-item--active.theme--dark .v-list-item__content {
  color: white;
  z-index: 1;
}

.v-window .v-toolbar {
  border-bottom: solid 1px black!important;
}

.v-card__text {
  font-size: 1rem !important;
}

.v-alert {
  font-size: 18px !important;
}

.v-navigation-drawer .v-list-item__action {
  margin: 12px 12px 12px 0px !important;
}

label.v-label--active div {
  color: white!important;
  font-weight: bold;
}

textarea {
  font-size: 1.2em!important;
  color: #FFF8E1!important;
}

.jp-Notebook,
.jp-OutputArea-output,
.jupyter-widgets,
.jp-Cell,
.jp-CodeCell,
.jp-Notebook-cell,
.jp-mod-noInput,
.jp-Cell-outputWrapper {
  margin: 0;
  padding: 0;
}

#cosmicds-app {
  height: 100%;
}

#app {
  height: 100vh;
  margin: 0;
  padding: 0;
}

.bqplot {
  height: 100%;
}

input {
  width: 4em !important;
  border-radius: 3px !important;
}

.MathJax,
.MathJax_Display {
  width: fit-content;
  height: fit-content;
}

mjx-container[jax="CHTML"][display="true"] {
  display: block !important;
}

/* issues with empty headers pushing WWT widget south, anyone else having this problem? -HOH */
.wwt_column {
  overflow-y: hidden;
}

.wwt_widget .v-toolbar {
  display: none;
}

.v-dialog.v-dialog--active .v-card__title,
.v-dialog.v-dialog--active .v-toolbar__content {
    cursor: grab;
}

.v-dialog.v-dialog--active .v-card__title.dragging,
.v-dialog.v-dialog--active .v-toolbar__content.dragging {
  cursor: grabbing;
}

.v-dialog > .v-card, #slideshow-root {
  border: solid hsla(0,0%,100%,.12) 1px !important;
}

.v-tooltip {
  z-index: 40;
}

/** Hide bqplot legend 'checkmark' symbols */
.g_legend path.line {
  display: none;
}

mjx-assistive-mml cds-input {
  display: none;
}

.icon-img {
  height: 40px !important;
  vertical-align: middle;
  margin: 2px;
}

</style>
