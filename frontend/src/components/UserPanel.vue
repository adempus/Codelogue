<template>
  <div class="p-grid p-ai-stretch vertical-container user_panel">
    <div class="p-col-3">
      <div class="box box-stretched">
        <FolderPane />
      </div>
    </div>
    <div class="p-col-9">
      <div class="box box-stretched">
        <PreviewPane />
      </div>
    </div>
  </div>
</template>

<script>
import FolderPane from "@/components/fragments/FolderPane";
import PreviewPane from "@/components/fragments/PreviewPane";

export default {
  name: "UserPanel",
  components: { FolderPane, PreviewPane }
};
</script>

<style scoped>
.user_panel {
  margin-top: 60px;
  padding: 0 2px 0px 2px;
}
</style>
