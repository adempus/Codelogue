<template>
  <div id="preview_pane">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "PreviewPane"
};
</script>

<style scoped>
#preview_pane {
  background-color: #272a36;
  height: 90vh !important;
  padding: 10px 15px 0 15px;
  overflow: hidden;
  border-radius: 5px;
}
</style>
