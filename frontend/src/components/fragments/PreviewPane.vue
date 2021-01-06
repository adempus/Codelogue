<template>
  <div class="p-shadow-3" id="preview_pane">
    <div v-if="previewSelection !== null">
      <div v-if="previewTargetIsFolder">
        <FolderPreview :folder-selection="previewTarget" />
      </div>
      <div v-else-if="previewTargetIsSnippet">
        <SnippetPreview :snippet-selection="previewTarget" />
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
  mounted() {
    this.$nextTick(() => {
      this.emitter.on("snippet-form-submitted", payload => {
        console.log("payload sent: ", payload);
        this.previewSelection = payload;
      });
      this.emitter.on("preview-selection", payload => {
        console.log("payload sent: ", payload);
        this.previewSelection = payload;
      });
    });
  },
  data() {
    return {
      previewSelection: null
    };
  },
  methods: {},
  computed: {
    previewTarget() {
      const sel = this.previewSelection;
      return {
        id: sel.key === undefined ? sel.id : sel.key,
        label: sel.label,
        type: sel.type
      };
    },
    previewTargetIsSnippet() {
      return this.previewTarget.type === "snippet";
    },
    previewTargetIsFolder() {
      return this.previewTarget.type === "folder";
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
