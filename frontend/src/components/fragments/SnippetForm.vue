<template>
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
        :placeholder="autoSelectedFolder['name']"
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
      <Chips id="tags" v-model="snippetForm.tags" style="height: 36px;" />
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
  mounted() {
    this.$nextTick(() => {
      // this.snippetForm.folder = this.selectedFolder;
      this.snippetForm.folder = this.autoSelectedFolder;
      // delay to initialize after api call
      setTimeout(() => {
        this.snippetForm.programmingLanguage = this.autoSelectedLanguage;
      }, 100);
    });
  },
  beforeUnmount() {
    this.resetValidations();
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (this.$v.$error) return;
      console.log("create snippet mutation");
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
    }
  }
};
</script>

<style scoped></style>
