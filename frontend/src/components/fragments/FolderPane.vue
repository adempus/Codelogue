<template>
  <ConfirmDeletionDialog
    :should-display="displayConfirmation"
    :deletion-selections="deletionList"
    @confirm-deletion="deleteSelectedFolders"
    @cancel-deletion="cancelDeletion"
  />
  <Card id="folder_pane">
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
              v-on:keyup.enter="createNewFolder()"
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
            style="height: 25px; width: 25px;"
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
      <ScrollPanel style="width: inherit; height: auto; margin-top: 15px;">
        <Tree
          :value="folders"
          id="folder_tree"
          v-model:selectionKeys="selectionKeys"
          :selectionMode="deleteMode ? 'checkbox' : 'single'"
          @node-select="updateDeletionSelection"
          @node-unselect="updateDeletionSelection"
        ></Tree>
      </ScrollPanel>
    </template>
  </Card>
</template>

<script>
import apolloClient from "@/graphql";
import { useMutation } from "@vue/apollo-composable";
import { required, minLength } from "@vuelidate/validators";
import userFoldersQuery from "@/graphql/queries/userFolders.query.graphql";
import createFolderMutation from "@/graphql/mutations/createFolder.mutation.graphql";
import deleteFoldersMutation from "@/graphql/mutations/deleteFolders.mutation.graphql";
import ConfirmDeletionDialog from "@/components/fragments/ConfirmDeletionDialog";

export default {
  name: "FolderPane",
  components: { ConfirmDeletionDialog },
  setup() {
    const { mutate: createFolder } = useMutation(createFolderMutation);
    const { mutate: deleteFolders } = useMutation(deleteFoldersMutation);
    return { createFolder, deleteFolders };
  },
  beforeMount() {
    this.queryUserFolders();
  },
  data() {
    return {
      folders: null,
      newFolderName: "",
      folderQueryResponse: null,
      folderMutationResponse: null,
      deleteMode: false,
      deletionList: [],
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
        .query({ query: { ...userFoldersQuery } })
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
            this.folders.push({
              key: this.folderMutationResponse["folder"]["id"],
              type: "folder",
              label: this.newFolderName,
              icon: "pi pi-fw pi-folder",
              children: []
            });
            this.newFolderName = "";
            this.$v.$reset();
          }
        });
    },
    parseFolderQueryResponse() {
      return this.folderQueryResponse.map(folder => {
        return {
          key: folder["id"],
          type: "folder",
          label: folder["name"],
          icon: "pi pi-fw pi-folder",
          children: folder["snippets"]["edges"].map(snippet => {
            return {
              key: snippet["node"]["id"],
              type: "snippet",
              parentKey: folder["id"],
              label: snippet["node"]["title"],
              icon: "pi pi-fw pi-file"
            };
          })
        };
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
    deleteSelectedFolders() {
      console.log("folders deleted!");
      const folderIds = this.folderDeletionIds;
      this.deleteFolders({ folderIds: folderIds })
        .then(res => {
          this.folderMutationResponse = res["data"]["deleteFolders"];
          console.log(res["data"]);
        })
        .catch(err => console.log("DeleteFolderMutation occurred. ", err))
        .finally(() => {
          if (!this.folderMutationResponse["status"]["error"]) {
            this.folders = this.folders.filter(item => {
              return !this.folderDeletionIds.includes(item.key);
            });
            this.finalizeDeletion();
          }
        });
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
    }
  }
};
</script>

<style scoped>
#folder_pane {
  background-color: #272a36;
  height: 90vh !important;
  padding: 15px 15px 20px 15px;
  overflow-y: auto;
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
  border-width: 3px;
}
#new_folder_name_input:focus {
  outline: none;
  box-shadow: none;
}
#folder_tree {
  background-color: #272a36;
  color: #d3d4d6;
  border: none;
  font-size: 14px;
  padding: 0px;
  outline: none !important;
  box-shadow: none;
}
#deleteFolderBtn {
  position: absolute;
  right: 12px;
  top: 56px;
  z-index: 100;
  background-color: #272a36;
  border-color: #6c757d;
}
#deleteFolderBtn:focus {
  outline: none;
  box-shadow: none;
}
</style>
