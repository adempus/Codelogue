<template>
  <ConfirmDeletionDialog
    :should-display="displayConfirmation"
    :deletion-selections="deletionList"
    @confirm-deletion="deleteFolders"
    @cancel-deletion="cancelDeletion"
  />
  <div id="folder_pane">
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
          />
          <Button
            icon="pi pi-plus-circle"
            class="p-button-warning"
            @click="createNewFolder()"
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
    <!-- folder tree section -->
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
  </div>
</template>

<script>
import apolloClient from "@/graphql";
import { useMutation } from "@vue/apollo-composable";
import { required, minLength } from "@vuelidate/validators";
import userFoldersQuery from "@/graphql/queries/userFolders.query.graphql";
import createFolderMutation from "@/graphql/mutations/createFolder.mutation.graphql";
import ConfirmDeletionDialog from "@/components/fragments/ConfirmDeletionDialog";

export default {
  name: "FolderPane",
  components: { ConfirmDeletionDialog },
  setup() {
    const { mutate: createFolder } = useMutation(createFolderMutation);
    return { createFolder };
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
      apolloClient.query({ query: { ...userFoldersQuery } }).then(res => {
        this.folderQueryResponse = res["data"]["getUserFolders"];
        this.folders = this.parseFolderQueryResponse(res);
      });
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
              label: this.newFolderName,
              icon: "pi pi-fw pi-folder"
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
      this.deletionList = this.folders.filter(folder => {
        if (folder.key in this.selectionKeys && folder.type === "folder") {
          let item = this.selectionKeys[folder.key];
          if (item.checked && !item.partialChecked) return folder;
        }
      });
      let snippets = this.folders.flatMap(folder => {
        return folder.children.filter(snippet => {
          let parent = snippet.parentKey;
          let parentPresent = parent in this.selectionKeys;
          if (parentPresent && this.selectionKeys[parent].partialChecked)
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
      if (!this.deleteMode && !this.deletionSelectionsEmpty) {
        this.selectionKeys = null;
        this.enableDeleteMode();
        this.showDeletionConfirmation();
      }
    },
    deleteFolders() {
      console.log("folders deleted!");
      this.finalizeDeletion();
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
    }
  },
  computed: {
    newFolderNameBlank() {
      return this.$v.newFolderName.required.$invalid;
    },
    deletionSelectionsEmpty() {
      return this.deletionList.length < 1;
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
  padding-bottom: 15px;
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
