<script>
export default {
  mounted() {
    const fetchScript = document.createElement("script");
    fetchScript.async = true;
    fetchScript.src = `https://www.googletagmanager.com/gtag/js?id=${this.tag}`;
    document.head.appendChild(fetchScript);

    const activateScript = document.createElement("script");
    activateScript.text = `window.dataLayer = window.dataLayer || [];
                           function gtag(){dataLayer.push(arguments);}
                           gtag('js', new Date());
                           gtag('config', "${this.tag}");`
    document.head.appendChild(activateScript);
  },

  props: {
    tag: {
      type: String,
      required: true,
    }
  }
}
</script>
