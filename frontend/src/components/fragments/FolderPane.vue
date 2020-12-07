<template>
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
            icon="pi pi-plus"
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
        />
      </div>
    </div>
    <!-- folder tree section -->
    <ScrollPanel style="width: inherit; height: auto; margin-top: 15px;">
      <Tree
        :value="folders"
        id="folder_tree"
        :selectionMode="deleteMode ? 'checkbox' : 'single'"
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

export default {
  name: "FolderPane",
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
      deleteMode: false
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
          label: folder["name"],
          icon: "pi pi-fw pi-folder",
          children: folder["snippets"]["edges"].map(snippet => {
            return {
              key: snippet["node"]["id"],
              label: snippet["node"]["title"],
              icon: "pi pi-fw pi-file"
            };
          })
        };
      });
    }
  },
  computed: {
    newFolderNameBlank() {
      return this.$v.newFolderName.required.$invalid;
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
  top: 60px;
  z-index: 100;
  background-color: #272a36;
  border-color: #6c757d;
}
#deleteFolderBtn:focus {
  outline: none;
  box-shadow: none;
}
</style>
