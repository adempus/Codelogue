<template>
  <Dialog
    v-model:visible="showMessage"
    header="Delete Content?"
    :style="{ width: '550px' }"
    :modal="true"
  >
    <div class="confirmation-content">
      <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
      <span v-if="folderCount !== 0 && snippetCount !== 0">{{
        bothDeletionMessage
      }}</span>
      <span v-else-if="folderCount !== 0">{{ folderDeletionMessage }}</span>
      <span v-else>{{ snippetDeletionMessage }}</span>
    </div>
    <template #footer>
      <Button
        label="No"
        icon="pi pi-times"
        @click="cancelDeletion"
        class="p-button-text"
      />
      <Button
        label="Yes"
        icon="pi pi-check"
        @click="confirmDeletion"
        class="p-button-text"
        autofocus
      />
    </template>
  </Dialog>
</template>

<script>
export default {
  props: {
    shouldDisplay: {
      type: Boolean,
      required: true
    },
    deletionSelections: {
      type: Array,
      required: true
    }
  },
  name: "ConfirmDeletionDialog",
  methods: {
    confirmDeletion() {
      this.$emit("confirm-deletion");
    },
    cancelDeletion() {
      this.$emit("cancel-deletion");
    }
  },
  computed: {
    showMessage() {
      return this.shouldDisplay;
    },
    getCount(item) {
      return this.deletionSelections.filter(selected => {
        return selected.type === item;
      }).length;
    },
    folderNoun() {
      return this.getCount("folder") > 1 ? "folders" : "folder";
    },
    snippetNoun() {
      return this.getCount("snippet") > 1 ? "snippets" : "snippet";
    },
    folderDeletionMessage() {
      return `Deleting a folder will also delete its contents.
      Continue deleting ${this.getCount("folder")} ${this.folderNoun}?`;
    },
    snippetDeletionMessage() {
      return `Continue deleting ${this.getCount("snippet")} ${this.snippetNoun}?`;
    },
    bothDeletionMessage() {
      return `You are about to delete ${this.getCount("folder")} ${this.folderNoun}
      and ${this.getCount("snippet")} separate ${this.snippetNoun}. Proceed?`;
    }
  }
};
</script>

<style scoped></style>
