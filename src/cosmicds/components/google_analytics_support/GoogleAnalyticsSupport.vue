<script>
export default {
  mounted() {
    const gaScript = document.createElement("script");
    gaScript.text = `
      // Logic derived from https://stackoverflow.com/a/61839170
      const local = (function (hostname=window.location.hostname) {
        return (
          (['localhost', '127.0.0.1', '', '::1'].includes(hostname))
          || (hostname.startsWith('192.168.'))
          || (hostname.startsWith('10.'))
        );
      })();
      if (!local) {
        const script = document.createElement("script");
        script.async = true;
        script.src = "https://www.googletagmanager.com/gtag/js?id=${this.tag}";
        document.head.appendChild(script);
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', "${this.tag}");
      }`
    document.head.appendChild(gaScript);
  },

  props: {
    tag: {
      type: String,
      required: true,
    }
  }
}
</script>
