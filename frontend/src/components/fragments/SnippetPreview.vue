<template>
  <div>
    <h2>Snippet</h2>
    {{ selectedSnippet }}
  </div>
</template>

<script>
export default {
  name: "SnippetPreview",
  props: {
    snippetSelection: {
      required: true,
      type: Object
    }
  },
  computed: {
    selectedSnippet() {
      return this.snippetSelection;
    },
    snippetId() {
      return this.snippetSelection.key;
    }
  }
};
</script>

<style scoped></style>
