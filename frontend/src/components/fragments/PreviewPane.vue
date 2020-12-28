<template>
  <div class="p-shadow-3" id="preview_pane">
    <div v-if="previewTarget !== null">
      <div v-if="previewTargetIsFolder">
        <FolderPreview :folder-selection="previewTargetId" />
      </div>
      <div v-else-if="previewTargetIsSnippet">
        <SnippetPreview :snippet-selection="previewTargetId" />
      </div>
    </div>
    <div v-else>
      <h2>Preview pane</h2>
    </div>
  </div>
</template>

<script>
import FolderPreview from "@/components/fragments/FolderPreview";
import SnippetPreview from "@/components/fragments/SnippetPreview";

export default {
  name: "PreviewPane",
  components: { SnippetPreview, FolderPreview },
  props: {
    previewSelection: {
      type: Object,
      required: true
    }
  },
  computed: {
    previewTarget() {
      return this.previewSelection;
    },
    previewTargetIsSnippet() {
      return this.previewSelection.type === "snippet";
    },
    previewTargetIsFolder() {
      return this.previewSelection.type === "folder";
    },
    previewTargetId() {
      return this.previewSelection;
    }
  }
};
</script>

<style scoped>
#preview_pane {
  background-color: #272a36;
  height: 90vh !important;
  padding: 15px 15px 0 25px;
  overflow: hidden;
  border-radius: 5px;
}
</style>
