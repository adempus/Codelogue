<template>
  <div id="preview_pane">
    <div v-if="previewTarget !== null">{{ previewTarget }}</div>
    <div v-else>Preview Pane</div>
  </div>
</template>

<script>
export default {
  name: "PreviewPane",
  props: {
    previewSelection: {
      type: Object,
      required: true
    }
  },
  computed: {
    previewTarget() {
      return this.previewSelection;
    }
  }
};
</script>

<style scoped>
#preview_pane {
  background-color: #272a36;
  height: 90vh !important;
}
</style>
