<script>
export default {
  mounted() {
    const gaScript = document.createElement('script');
    gaScript.async = true;
    gaScript.src = `https://www.googletagmanager.com/gtag/js?id=${this.tag}`;
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
