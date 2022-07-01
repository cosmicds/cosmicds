<template>
  <v-textarea
    v-model="response"
    auto-grow
    filled
    color="deep-purple"
    rows="1"
    hint="type your response here"
  >
    <template v-slot:label>
      <div>{{ questionLabel }}</div>
    </template>
  </v-textarea>
</template>

<script>
module.exports = {
  props: ["questionLabel"],
  data: function () {
    return {
      response: "",
    };
  },
};
</script>