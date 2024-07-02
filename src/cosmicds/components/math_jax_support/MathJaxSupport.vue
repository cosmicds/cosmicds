<script>
export default {
  async mounted() {
    if (!window.customElements.get("cds-input")) {

      class CustomInput extends HTMLElement {

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
          // if (tag) {
          //   const application = CustomInput.app;
          //   if (tag in application.story_state.inputs) {
          //     this.input.value = application.story_state.inputs[tag];
          //   }
          // }
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
          if (!tag) {
            return;
          }
          // const application = CustomInput.app;
          // application.story_state.inputs[tag] = text;
          // AFAICT, we need to call this here to update the state Python-side
          // app.update_state();
        }
      }

      window.customElements.define("cds-input", CustomInput);
    } else {
      const inputClass = window.customElements.get("cds-input");
    }

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
    console.log("Attempting load of mathjax.")
    await new Promise((resolve, reject) => {
      const mathJaxScript = document.createElement('script');
      mathJaxScript.async = true;
      mathJaxScript.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js";
      document.head.appendChild(mathJaxScript);
      mathJaxScript.onload = (_e) => resolve();
      mathJaxScript.onerror = (_e) => reject();
      console.log("MathJax start up finished.")
    });
    await MathJax.startup.promise;

    // Not all of our elements are initially in the DOM,
    // so we need to account for that in order to get MathJax
    // to render their formulae properly
    const mathJaxOpeningDelimiters = ["$$", "\\(", "\\["];
    const containsMathJax = node => mathJaxOpeningDelimiters.some(delim => node.innerHTML.includes(delim));
    const elementToScan = node => node.nodeType === Node.ELEMENT_NODE;
    const mathJaxCallback = function (mutationList, _observer) {
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
    const options = {childList: true, subtree: true};
    observer.observe(this.$el, options);
  },
}
</script>

<template>
</template>