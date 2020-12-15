<template>
  <div class="p-grid p-ai-stretch vertical-container user_panel">
    <div class="p-col-3">
      <div class="box box-stretched">
        <FolderPane @preview-selection="previewSelected"></FolderPane>
      </div>
    </div>
    <div class="p-col-9">
      <div class="box box-stretched">
        <SnippetPane :preview-selection="previewTarget"></SnippetPane>
      </div>
    </div>
  </div>
</template>

<script>
import FolderPane from "@/components/fragments/FolderPane";
import SnippetPane from "@/components/fragments/SnippetPane";

export default {
  name: "UserPanel",
  components: { FolderPane, SnippetPane },
  data() {
    return {
      previewTarget: {}
    };
  },
  methods: {
    previewSelected(previewTarget) {
      this.previewTarget = previewTarget;
      console.log("an item has been selected in folder pane: ", previewTarget);
    }
  }
};
</script>

<style scoped>
.user_panel {
  margin-top: 60px;
  padding: 0 5px 0px 5px;
}
</style>
