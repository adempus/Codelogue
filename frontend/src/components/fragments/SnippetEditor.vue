<template style="overflow-x: hidden">
  <div v-if="editModeNew">
    <div class="p-d-flex p-jc-between">
      <div class="p-flex-column">
        <div class="p-mb-2">
          <p style="margin-top: 0; font-size: 50px;">New Snippet</p>
        </div>
      </div>
      <div>
        <!-- cancel button -->
        <Button
          label="Cancel"
          icon="pi pi-times"
          iconPos="left"
          class="p-button-outlined p-button-danger p-button-raised"
          id="cancel_snippet_btn"
          @click="cancelEdit"
        />
      </div>
    </div>
    <div class="p-fluid p-formgrid p-grid" style="margin-top: -20px;">
      <!-- title input -->
      <div class="p-field p-col-12 p-md-4">
        <div class="p-grid p-jc-start p-md-1">
          <label for="title">Title</label>
        </div>
        <InputText
          v-model="snippetForm.title"
          id="title"
          type="text"
          aria-describedby="title-help"
        />
        <!-- title required error notice -->
        <div class="p-grid p-jc-start p-md-12">
          <small
            v-if="snippetTitleBlank"
            id="title-help"
            class="p-invalid p-mt-1"
            >Title cannot be blank</small
          >
        </div>
      </div>
      <!-- folder dropdown -->
      <div class="p-field p-col-12 p-md-2" style="margin-left: 460px;">
        <div class="p-grid p-jc-start p-md-1">
          <label for="folder">Folder</label>
        </div>
        <Dropdown
          id="folder"
          v-model="snippetForm.folder"
          :options="folderOptions"
          scrollHeight="275px"
          optionLabel="name"
          :placeholder="selectedFolder['name']"
          :filter="true"
          aria-describedby="folder-help"
        >
          <!-- templating to left align dropdown options -->
          <template #value="slotProps">
            <div class="p-d-flex">
              <div>{{ slotProps.value.name }}</div>
            </div>
          </template>
          <template #option="slotProps">
            <div class="p-d-flex">
              <div>{{ slotProps.option.name }}</div>
            </div>
          </template>
        </Dropdown>
        <!-- folder required error notice -->
        <div class="p-grid p-jc-start p-md-12">
          <small
            v-if="snippetFolderNotSelected"
            id="folder-help"
            class="p-invalid p-mt-1"
            >Must select a folder</small
          >
        </div>
      </div>
      <div class="p-field p-col-12 p-md-2">
        <!-- programming language dropdown -->
        <div class="p-grid p-jc-start p-md-12">
          <label for="folder">Programming Language</label>
        </div>
        <Dropdown
          id="language"
          v-model="snippetForm.programmingLanguage"
          :options="languageOptions"
          scrollHeight="275px"
          optionLabel="name"
          :filter="true"
          aria-describedby="language-help"
        >
          <!-- templating to left align dropdown options -->
          <template #value="slotProps">
            <div class="p-d-flex">
              <div v-if="Object.keys(slotProps.value).length === 0">
                Select
              </div>
              <div v-else>{{ slotProps.value.name }}</div>
            </div>
          </template>
          <template #option="slotProps">
            <div class="p-d-flex">
              <div>{{ slotProps.option.name }}</div>
            </div>
          </template>
        </Dropdown>
        <!-- programming language required error notice -->
        <div class="p-grid p-jc-start p-md-12">
          <small
            v-if="snippetLanguageNotSelected"
            id="language-help"
            class="p-invalid p-mt-1"
            >Must select a language</small
          >
        </div>
      </div>
      <!-- code editor -->
      <div class="p-field p-col-12 p-md-12">
        <div class="p-grid p-jc-start p-md-1">
          <label for="content">Content</label>
        </div>
        <Editor
          v-model="snippetForm.content"
          id="content"
          editorStyle="height: 300px;"
          placeholder="Type code here"
          aria-describedby="content-help"
        >
          <template #toolbar></template>
        </Editor>
        <div class="p-grid p-jc-start p-md-12">
          <small
            v-if="snippetContentBlank"
            id="content-help"
            class="p-invalid p-mt-1"
            >Content cannot be blank</small
          >
        </div>
      </div>
      <!-- description editor -->
      <div class="p-field p-col-12 p-md-12">
        <div class="p-grid p-jc-start p-md-1">
          <label for="description">Description</label>
        </div>
        <Textarea
          id="description"
          v-model="snippetForm.description"
          :autoResize="true"
          style="height: 500px;"
          rows="5"
        />
      </div>
      <!-- tags input -->
      <div class="p-field p-col-12 p-md-12">
        <div class="p-grid p-jc-start p-md-1">
          <label for="tags">Tags</label>
        </div>
        <Chips id="tags" v-model="snippetForm.tags" style="height: 36px;" />
      </div>
      <!-- submit button -->
      <div class="p-field p-col-12 p-md-12">
        <div class="p-d-flex p-jc-end">
          <div>
            <Button
              label="Submit"
              icon="pi pi-check"
              iconPos="left"
              class="p-button-outlined p-button-success p-button-raised"
              id="submit_snippet_btn"
              @click="submit"
            ></Button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else-if="editModeModify">
    <h1>Modify Snippet</h1>
  </div>
</template>

<script>
import { useQuery, useResult } from "@vue/apollo-composable";
import folderAndLanguageOptions from "@/graphql/queries/folderAndLanguageOptions.query.graphql";
import { required } from "@vuelidate/validators";

export default {
  name: "SnippetEditor",
  setup() {
    const { result } = useQuery(folderAndLanguageOptions);
    const folderQueryResult = useResult(
      result,
      null,
      data => data["getUserFolders"]
    );
    const languageQueryResult = useResult(
      result,
      null,
      data => data["allLanguages"]["edges"]
    );
    return { folderQueryResult, languageQueryResult };
  },
  mounted() {
    this.snippetForm.folder = this.selectedFolder;
  },
  beforeUnmount() {
    this.$v.$reset();
  },
  props: {
    editMode: {
      required: true,
      type: Object
    },
    targetFolder: {
      required: false,
      type: Object
    }
  },
  data() {
    return {
      snippetForm: {
        title: "",
        folder: {},
        programmingLanguage: {},
        content: "",
        description: "",
        tags: []
      }
    };
  },
  validations() {
    return {
      snippetForm: {
        title: { required },
        folder: { required },
        programmingLanguage: { required },
        content: { required }
      }
    };
  },
  methods: {
    cancelEdit() {
      this.$emit("cancel-edit");
    },
    submit() {
      this.$v.$touch();
      if (this.$v.$error) return;
      console.log("create snippet mutation");
    }
  },
  computed: {
    editModeNew() {
      return this.editMode.newSnippet;
    },
    editModeModify() {
      return this.editMode.modifySnippet;
    },
    selectedFolder() {
      return {
        id: this.targetFolder["key"],
        name: this.targetFolder["label"]
      };
    },
    folderOptions() {
      if (this.folderQueryResult === null) return [];
      return this.folderQueryResult;
    },
    languageOptions() {
      if (this.languageQueryResult === null) return [];
      return this.languageQueryResult.map(lang => {
        return {
          id: lang["node"]["id"],
          name: lang["node"]["name"]
        };
      });
    },
    snippetTitleBlank() {
      return this.$v.snippetForm.title.required.$invalid;
    },
    snippetContentBlank() {
      return this.$v.snippetForm.content.required.$invalid;
    },
    snippetFolderNotSelected() {
      return this.$v.snippetForm.folder.required.$invalid;
    },
    snippetLanguageNotSelected() {
      return this.$v.snippetForm.programmingLanguage.required.$invalid;
    }
  }
};
</script>

<style scoped>
.form-label {
  float: left;
}
.p-editor-toolbar {
}
#cancel_snippet_btn {
  margin-top: 15px;
  margin-right: 15px;
  font-weight: bold;
}
#submit_snippet_btn {
  font-weight: bold;
}
</style>
