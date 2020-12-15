<template>
  <div class="p-grid p-ai-stretch vertical-container user_panel">
    <div class="p-col-3">
      <div class="box box-stretched">
        <FolderPane @preview-selection="previewSelected"></FolderPane>
      </div>
    </div>
    <div class="p-col-9">
      <div class="box box-stretched">
        <PreviewPane :preview-selection="previewTarget"></PreviewPane>
      </div>
    </div>
  </div>
</template>

<script>
import FolderPane from "@/components/fragments/FolderPane";
import PreviewPane from "@/components/fragments/PreviewPane";

export default {
  name: "UserPanel",
  components: { FolderPane, PreviewPane },
  data() {
    return {
      previewTarget: null
    };
  },
  methods: {
    previewSelected(previewTarget) {
      this.previewTarget = previewTarget;
      // console.log("an item has been selected in folder pane: ", previewTarget);
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
