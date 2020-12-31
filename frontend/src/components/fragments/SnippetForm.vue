<template>
  <Toast position="top-right" />
  <form class="p-fluid p-formgrid p-grid" style="margin-top: -10px;">
    <!-- title input -->
    <div class="p-field p-col-12 p-md-4">
      <div class="p-grid p-jc-start p-ml-1 p-mb-2">
        <label for="title">Title</label>
      </div>
      <InputText
        v-model="snippetForm.title"
        :class="{ 'p-invalid': snippetTitleBlank }"
        id="title"
        type="text"
        aria-describedby="title-help"
      />
      <!-- title required error notice -->
      <div class="p-grid p-jc-start p-md-12">
        <small v-if="snippetTitleBlank" id="title-help" class="p-invalid p-mt-1"
          >Title cannot be blank</small
        >
      </div>
    </div>
    <!-- folder dropdown -->
    <div class="p-field p-col-12 p-md-2" style="margin-left: 460px;">
      <div class="p-grid p-jc-start p-ml-1 p-mb-2">
        <label for="folder">Folder</label>
      </div>
      <Dropdown
        id="folder"
        :class="{ 'p-invalid': snippetFolderNotSelected }"
        v-model="snippetForm.folder"
        :options="folderOptions"
        scrollHeight="275px"
        optionLabel="name"
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
      <div class="p-grid p-jc-start p-ml-1 p-mb-2">
        <label for="folder">Programming Language</label>
      </div>
      <Dropdown
        id="language"
        :class="{ 'p-invalid': snippetLanguageNotSelected }"
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
      <div class="p-grid p-jc-start p-ml-1 p-mb-2">
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
      <div class="p-grid p-jc-start p-ml-1 p-mb-2">
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
      <div class="p-grid p-jc-start p-ml-1 p-mb-2">
        <label for="tags">Tags</label>
      </div>
      <Chips
        id="tags"
        v-model="snippetForm.tags"
        :allowDuplicate="false"
        style="height: 36px;"
      />
    </div>
    <!-- submit button -->
    <div class="p-field p-col-12 p-md-12">
      <div class="p-d-flex p-jc-end">
        <div>
          <Button
            label="Done"
            icon="pi pi-check-circle"
            iconPos="left"
            class="p-button-warning p-button-raised"
            id="submit_snippet_btn"
            @click="submit"
          ></Button>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
import { required } from "@vuelidate/validators";
import { useMutation } from "@vue/apollo-composable";
import createSnippetMutation from "@/graphql/mutations/createSnippet.mutation.graphql";
import createTagsMutation from "@/graphql/mutations/createTags.mutation.graphql";
import createTaggedSnippetMutation from "@/graphql/mutations/createTaggedSnippet.mutation.graphql";

export default {
  name: "SnippetForm",
  props: {
    foldersQueryResult: {
      required: true,
      type: Array
    },
    languagesQueryResult: {
      required: true,
      type: Array
    },
    defaultFolder: {
      required: true,
      type: Object
    },
    defaultLanguage: {
      required: true,
      type: Object
    },
    snippetQueryResult: {
      // only required if a snippet is being updated
      required: false,
      type: Object
    }
  },
  setup() {
    const { mutate: createSnippet } = useMutation(createSnippetMutation);
    const { mutate: createTags } = useMutation(createTagsMutation);
    const { mutate: createTaggedSnippet } = useMutation(
      createTaggedSnippetMutation
    );
    return { createSnippet, createTags, createTaggedSnippet };
  },
  mounted() {
    this.$nextTick(() => {
      this.snippetForm.folder = this.autoSelectedFolder;
      // delay to initialize after api call
      setTimeout(() => {
        this.snippetForm.programmingLanguage = this.autoSelectedLanguage;
      }, 250);
    });
  },
  beforeUnmount() {
    this.resetValidations();
  },
  data() {
    return {
      snippetId: null,
      snippetForm: {
        title: "",
        folder: {},
        programmingLanguage: {},
        content: "",
        description: "",
        tags: []
      },
      snippetMutationResponse: {},
      tagsMutationResponse: { tags: [] },
      createSnippetSuccess: false
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
    submit() {
      this.$v.$touch();
      if (this.$v.$error) return;
      this.createNewSnippet();
    },
    createNewSnippet() {
      const newSnippet = this.newSnippetPayload;
      console.log("payload: ", newSnippet);
      this.createSnippet({ input: newSnippet })
        .then(res => {
          this.snippetMutationResponse.status =
            res["data"]["createSnippet"]["status"];
          this.snippetMutationResponse.snippet =
            res["data"]["createSnippet"]["snippet"];
        })
        .catch(err => console.log("CreateSnippetMutation error.", err))
        .finally(() => {
          if (!this.snippetMutationResponse.status.error) {
            if (this.snippetForm.tags.length > 0) {
              this.createOrGetTags();
            } else {
              this.showSuccessMessage();
              this.navToFolderPreview();
            }
            console.log("snippet mutation completed");
          }
        });
    },
    createOrGetTags() {
      const tags = this.snippetForm.tags;
      this.createTags({ keywords: tags })
        .then(res => {
          this.tagsMutationResponse.tags = res["data"]["createTags"]["tags"];
        })
        .catch(err => console.log("CreateTagsMutation error.", err))
        .finally(() => {
          if (this.tagsMutationResponse.tags.length > 0) {
            console.log("tags mutation complete");
            this.saveSnippetTags();
          }
        });
    },
    saveSnippetTags() {
      const snippetId = this.snippetMutationResponse.snippet.id;
      const tagIds = this.tagsMutationResponse.tags.map(tag => {
        return tag["id"];
      });
      this.createTaggedSnippet({ snippetId: snippetId, tagIds: tagIds })
        .then(res => {
          this.createSnippetSuccess = !("error" in res);
        })
        .finally(() => {
          if (this.createSnippetSuccess) {
            console.log("snippet tags mutation complete!");
            this.showSuccessMessage();
            this.navToFolderPreview();
            return;
          }
          console.log("show error message");
        });
    },
    updateExistingSnippet() {},
    showSuccessMessage() {
      this.$toast.add({
        severity: "success",
        summary: `Created new snippet: ${this.snippetForm.title}`,
        life: 2000
      });
    },
    navToFolderPreview() {
      setTimeout(() => {
        this.$emit("new-submission-complete");
      }, 1000);
    },
    resetValidations() {
      this.$v.snippetForm.title.$dirty = false;
      this.$v.snippetForm.content.$dirty = false;
      this.$v.snippetForm.folder.$dirty = false;
      this.$v.snippetForm.programmingLanguage.$dirty = false;
    }
  },
  computed: {
    snippetTitleBlank() {
      return (
        this.snippetForm.title.trim().length === 0 &&
        this.$v.snippetForm.title.$dirty
      );
    },
    snippetContentBlank() {
      return (
        this.snippetForm.content.trim().length === 0 &&
        this.$v.snippetForm.content.$dirty
      );
    },
    snippetFolderNotSelected() {
      return (
        Object.keys(this.snippetForm.folder).length === 0 &&
        this.$v.snippetForm.folder.$dirty
      );
    },
    snippetLanguageNotSelected() {
      return (
        Object.keys(this.snippetForm.programmingLanguage).length === 0 &&
        this.$v.snippetForm.programmingLanguage.$dirty
      );
    },
    folderOptions() {
      return this.foldersQueryResult;
    },
    autoSelectedFolder() {
      return this.defaultFolder;
    },
    languageOptions() {
      return this.languagesQueryResult;
    },
    autoSelectedLanguage() {
      return this.defaultLanguage;
    },
    tagsFilled() {
      return this.snippetForm.tags.length > 0;
    },
    loadedSnippet() {
      return this.snippetQueryResult;
    },
    newSnippetPayload() {
      return {
        title: this.snippetForm.title,
        folderId: this.snippetForm.folder.id,
        languageId: this.snippetForm.programmingLanguage.id,
        content: this.snippetForm.content,
        description: this.snippetForm.description
      };
    }
  }
};
</script>

<style scoped>
#title,
#folder,
#language,
#description {
  border-width: 1px;
  color: #ffffff;
  border-color: #454a5e;
  background-color: #313645;
}
</style>
<style>
input#tags {
  color: #ffffff;
}
.p-inputtext.p-chips-multiple-container {
  background-color: #313645;
  border-color: #454a5e;
  color: #ffffff;
}
.p-editor-container .p-editor-content .ql-editor {
  background-color: #313645 !important;
  border-color: #454a5e !important;
  color: #ffffff !important;
}
.ql-editor.ql-blank::before {
  color: #ffffff !important;
}
.p-editor-toolbar.ql-toolbar.ql-snow {
  border-color: #454a5e !important;
  background-color: #454a5e !important;
}
.p-editor-content.ql-container.ql-snow {
  height: 300px !important;
  border-color: #454a5e !important;
}
.p-dropdown-label.p-inputtext {
  color: #ffffff !important;
}
</style>
