<template>
  <div id="snippet_pane">{{ previewObject }}</div>
</template>

<script>
export default {
  name: "SnippetPane",
  props: {
    previewSelection: {
      type: Object,
      required: true
    }
  },
  computed: {
    previewObject() {
      return this.previewSelection;
    }
  }
};
</script>

<style scoped>
#snippet_pane {
  background-color: #272a36;
  height: 90vh !important;
}
</style>
