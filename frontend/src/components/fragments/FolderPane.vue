<template>
    <Toast class="p-ml-3 p-align-start" position="bottom-left" />
    <ConfirmDeletionDialog
            :should-display="displayConfirmation"
            :deletion-selections="deletionList"
            @confirm-deletion="deleteSelected"
            @cancel-deletion="cancelDeletion"
    />
    <Card class="p-shadow-3" id="folder_pane">
        <template v-slot:header>
            <div class="p-grid p-fluid">
                <!-- new folder input form -->
                <div class="p-col-12" style="position: relative;">
                    <div
                            id="new_folder_form"
                            class="p-inputgroup"
                            style="position: sticky;"
                    >
                        <InputText
                                placeholder="New Folder"
                                v-model="newFolderName"
                                id="new_folder_name_input"
                                :class="{ 'p-invalid': newFolderNameBlank }"
                                aria-describedby="cannot_be_blank_error"
                                v-on:keypress.enter="createNewFolder()"
                                :disabled="deleteMode"
                        />
                        <Button
                                icon="pi pi-plus-circle"
                                class="p-button-warning"
                                @click="createNewFolder()"
                                :disabled="deleteMode"
                        />
                    </div>
                </div>
                <!-- blank folder name error msg -->
                <small
                        v-if="newFolderNameBlank"
                        id="cannot_be_blank_error"
                        class="p-invalid"
                >Folder name is required</small
                >
                <div style="position: relative;">
                    <ToggleButton
                            v-model="deleteMode"
                            id="deleteFolderBtn"
                            class="p-button-sm"
                            onIcon="pi pi-check"
                            offIcon="pi pi-trash"
                            @change="handleDeletionAction"
                    />
                </div>
            </div>
        </template>
        <!-- folder tree section -->
        <template v-slot:content>
            <ScrollPanel id="folder_list">
                <Tree
                        :value="folders"
                        id="folder_tree"
                        v-model:selectionKeys="selectionKeys"
                        :selectionMode="deleteMode ? 'checkbox' : 'single'"
                        @node-select="handleSelectionAction"
                        @node-unselect="handleSelectionAction"
                ></Tree>
            </ScrollPanel>
        </template>
    </Card>
</template>

<script>
import apolloClient from "@/graphql";
import { useMutation } from "@vue/apollo-composable";
import { required, minLength } from "@vuelidate/validators";
import getFolders from "@/graphql/queries/getFolders.query.graphql";
import createFolderMutation from "@/graphql/mutations/createFolder.mutation.graphql";
import deleteFoldersMutation from "@/graphql/mutations/deleteFolders.mutation.graphql";
import ConfirmDeletionDialog from "@/components/fragments/ConfirmDeletionDialog";

export default {
  name: "FolderPane",
  components: { ConfirmDeletionDialog },
  emits: ["preview-selection"],
  setup() {
    const { mutate: createFolder } = useMutation(createFolderMutation);
    const { mutate: deleteFolders } = useMutation(deleteFoldersMutation);
    return { createFolder, deleteFolders };
  },
  beforeMount() {
    this.$nextTick(() => {
      this.queryUserFolders();
    });
  },
  mounted() {
    this.$nextTick(() => {
      this.appendNewSnippet();
    });
  },
  data() {
    return {
      folders: null,
      newFolderName: "",
      folderQueryResponse: null,
      folderMutationResponse: null,
      deleteMode: false,
      deletionList: [],
      previewTarget: null,
      selectionKeys: [],
      displayConfirmation: false
    };
  },
  validations() {
    return {
      newFolderName: {
        required,
        minLength: minLength(3)
      }
    };
  },
  methods: {
    queryUserFolders() {
      apolloClient
        .query({ query: { ...getFolders } })
        .then(res => {
          this.folderQueryResponse = res["data"]["getUserFolders"];
          this.folders = this.parseFolderQueryResponse(res);
        })
        .catch(err => console.log("UserFoldersQuery error occurred.", err));
    },
    createNewFolder() {
      this.$v.$touch();
      if (this.$v.$error) return;
      this.createFolder({ name: this.newFolderName.trim() })
        .then(
          res => (this.folderMutationResponse = res["data"]["createFolder"])
        )
        .catch(err => console.log("CreateFolderMutation error.", err))
        .finally(() => {
          if (!this.folderMutationResponse["status"]["error"]) {
            const newFolder = {
              key: this.folderMutationResponse["folder"]["id"],
              type: "folder",
              label: this.newFolderName,
              icon: "pi pi-fw pi-folder",
              children: []
            };
            this.folders.push(newFolder);
            this.notifyNewFolderSuccess();
            this.newFolderName = "";
            this.$v.$reset();
            this.handleSelectionAction(newFolder); // preview new folder
          }
        });
    },
    appendNewSnippet() {
      this.emitter.on("snippet-creation-success", payload => {
        const snippet = payload;
        this.folders.map(folder => {
          const parentKey = snippet.folder.id;
          if (folder.key === parentKey) {
            folder.children.push(
              this.getSnippetObject(snippet.id, snippet.title, parentKey)
            );
          }
        });
      });
    },
    notifyNewFolderSuccess() {
      this.$toast.add({
        severity: "success",
        summary: "Folder Created",
        detail: `Added new folder: ${this.newFolderName}`,
        life: 1300
      });
    },
    parseFolderQueryResponse() {
      return this.folderQueryResponse.map(folder => {
        return this.getFolderObject(
          folder["id"],
          folder["name"],
          folder["snippets"]["edges"].map(snippet => {
            return this.getSnippetObject(
              snippet["node"]["id"],
              snippet["node"]["title"],
              folder["id"]
            );
          })
        );
      });
    },
    getFolderObject(key, label, children) {
      return {
        key: key,
        type: "folder",
        label: label,
        children: children,
        icon: "pi pi-fw pi-folder"
      };
    },
    getSnippetObject(key, label, parentKey) {
      return {
        key: key,
        type: "snippet",
        parentKey: parentKey,
        label: label,
        icon: "pi pi-fw pi-file"
      };
    },
    handleSelectionAction(node) {
      if (this.previewMode) {
        if (node.type === "folder") {
          this.navToPreview("FolderPreview", node.key);
        } else if (node.type === "snippet") {
          this.navToPreview("SnippetPreview", node.key);
        }
        return;
      }
      if (this.deleteMode) this.updateDeletionSelection();
    },
    navToPreview(previewType, previewId) {
      this.$router.push({
        name: previewType,
        params: { id: previewId }
      });
    },
    updateDeletionSelection() {
      if (!this.deleteMode) return;
      // collect folders
      this.deletionList = this.folders.filter(folder => {
        if (folder.key in this.selectionKeys && folder.type === "folder") {
          let selectedFolder = this.selectionKeys[folder.key];
          // if a folder itself is selected, all of its contents are as well. Return the folder exclusively.
          if (selectedFolder.checked && !selectedFolder.partialChecked)
            return selectedFolder;
        }
      });
      // collect snippets
      let snippets = this.folders.flatMap(folder => {
        return folder.children.filter(snippet => {
          let parentFolder = snippet.parentKey;
          let parentSelected = parentFolder in this.selectionKeys;
          // if some folder's contents are selected but not the folder itself, return its selected contents exclusively.
          if (parentSelected && this.selectionKeys[parentFolder].partialChecked)
            return snippet.key in this.selectionKeys;
        });
      });
      this.deletionList = this.deletionList.concat(snippets);
    },
    removeNode(node) {
      this.deletionList = this.deletionList.filter(selected => {
        return selected !== node;
      });
    },
    clearDeletionSelections() {
      this.selectionKeys = [];
      this.deletionList = [];
    },
    handleDeletionAction() {
      // confirmation to be shown when deletion is toggled off
      if (!this.deleteMode && !this.deletionSelectionsEmpty) {
        this.enableDeleteMode();
        this.showDeletionConfirmation();
      }
    },
    deleteSelected() {
      const folderIds = this.folderDeletionIds;
      this.deleteFolders({ folderIds: folderIds })
        .then(res => {
          this.folderMutationResponse = res["data"]["deleteFolders"];
        })
        .catch(err => console.log("DeleteFolderMutation occurred. ", err))
        .finally(() => {
          // console.log("check: ", this.folderMutationResponse);
          if (!this.folderMutationResponse["status"]["error"]) {
            // update UI
            this.folders = this.folders.filter(folder => {
              return !this.folderDeletionIds.includes(folder.key);
            });
            this.notifyFolderDeletionSuccess();
            this.finalizeDeletion();
          }
        });
    },
    notifyFolderDeletionSuccess() {
      const numDeleted = this.folderDeletionIds.length;
      this.$toast.add({
        severity: "success",
        summary: "Folder Deleted",
        detail: `Deleted ${numDeleted} ${
          numDeleted > 1 ? "folders" : "folder"
        }`,
        life: 1250
      });
    },
    clearDeletedInPreview() {
      if (this.previewTarget === null) return;
      const targetId = this.previewTarget.key;
      if (
        this.folderDeletionIds.includes(targetId) ||
        this.snippetDeletionIds.includes(targetId)
      ) {
        this.emitter.emit("clear-deleted-in-preview");
      }
    },
    cancelDeletion() {
      this.finalizeDeletion();
    },
    showDeletionConfirmation() {
      this.displayConfirmation = true;
    },
    hideDeletionConfirmation() {
      this.displayConfirmation = false;
    },
    enableDeleteMode() {
      this.deleteMode = true;
    },
    disableDeleteMode() {
      this.deleteMode = false;
    },
    finalizeDeletion() {
      this.clearDeletedInPreview();
      this.hideDeletionConfirmation();
      this.clearDeletionSelections();
      this.disableDeleteMode();
    },
    filterDeletionIds(type) {
      return this.deletionList
        .filter(selected => {
          return selected.type === type;
        })
        .map(item => {
          return item.key;
        });
    }
  },
  computed: {
    newFolderNameBlank() {
      return this.$v.newFolderName.required.$invalid;
    },
    deletionSelectionsEmpty() {
      return this.deletionList.length < 1;
    },
    folderDeletionIds() {
      return this.filterDeletionIds("folder");
    },
    snippetDeletionIds() {
      return this.filterDeletionIds("snippet");
    },
    previewMode() {
      return !this.deleteMode;
    }
  }
};
</script>

<style scoped>
#folder_pane {
    background-color: #272a36;
    height: 90vh !important;
    padding: 15px 15px 0 15px;
    overflow-y: hidden;
    border-radius: 5px;
}
#new_folder_form {
    padding-bottom: 0;
}
#cannot_be_blank_error {
    position: absolute;
    margin-top: 55px;
    padding-left: 10px;
}
#new_folder_name_input {
    border-width: 2px;
}
#new_folder_name_input:focus {
    outline: none;
    box-shadow: none;
}
#folder_tree {
    background-color: inherit;
    color: #d3d4d6;
    border: none;
    font-size: 14px;
    padding: 0px;
    outline: none !important;
    box-shadow: none;
}
#deleteFolderBtn {
    height: 35px;
    width: 35px;
    position: absolute;
    right: 10px;
    top: 56px;
    z-index: 100;
    background-color: #272a36;
    border-color: #6c757d;
}
#deleteFolderBtn:focus {
    outline: none;
    box-shadow: none;
}
#folder_list {
    width: 107%;
    height: 75vh;
    margin-top: 15px;
    padding-right: 10px;
}
</style>
<style>
#folder_list.p-scrollpanel .p-scrollpanel-bar {
    width: 4px !important;
    /*background-color: #3c4049 !important;*/
    background-color: #6c757d !important;
    opacity: 1;
    transition: background-color 0.2s;
}
.p-scrollpanel-bar:hover {
    background-color: #6c757d !important;
    /*background-color: #51545e !important;*/
}
.p-treenode-content:hover {
    /*background-color: #464d63 !important;*/
    background-color: #323645 !important;
    color: #ffffff !important;
}
.p-treenode-content:active {
    /*background-color: #464d63 !important;*/
    background-color: #61667b !important;
    color: #ffffff !important;
}
.p-treenode-content:focus {
    /*background-color: #464d63 !important;*/
    background-color: #323645 !important;
    color: #ffffff !important;
    outline: none !important;
    box-shadow: none !important;
}
.p-highlight {
    /*background-color: #464d63 !important;*/
    background-color: #323645 !important;
    color: #ffffff !important;
}
.p-treenode-icon {
    color: #6c757d !important;
}
.p-toast-message-text {
    text-align: left !important;
}
</style>
