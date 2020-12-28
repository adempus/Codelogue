<template>
  <div v-if="editModeNew">
    <div class="p-d-flex p-jc-between">
      <div class="p-flex-column">
        <div class="p-mb-2">
          <p style="margin-top: 0; font-size: 50px;">New Snippet</p>
        </div>
      </div>
      <div>
        <Button
          label="Cancel"
          icon="pi pi-times"
          iconPos="left"
          class="p-button-outlined p-button-danger p-button-raised"
          id="cancel_snippet_btn"
          @click="cancelEdit()"
        />
      </div>
    </div>
    <div class="p-fluid p-formgrid p-grid">
      <!-- snippet title -->
      <div class="p-field p-col-12 p-md-4">
        <div class="p-grid p-jc-start p-md-1">
          <label for="title">Title</label>
        </div>
        <InputText id="title" type="text" />
      </div>
      <!-- snippet folder -->
      <div class="p-field p-col-12 p-md-2" style="margin-left: 460px;">
        <div class="p-grid p-jc-start p-md-1">
          <label for="folder">Folder</label>
        </div>
        <Dropdown
          id="folder"
          v-model="snippetForm.folder"
          :options="options.folders"
          :scrollHeight="200"
          optionLabel="name"
          placeholder="Folder"
          :filter="true"
        />
      </div>
      <div class="p-field p-col-12 p-md-2">
        <div class="p-grid p-jc-start p-md-12">
          <label for="folder">Programming Language</label>
        </div>
        <Dropdown
          id="language"
          v-model="snippetForm.programmingLanguage"
          :options="options.programmingLanguages"
          optionLabel="Programming Language"
          placeholder="Language"
          :filter="true"
        />
      </div>
      <div class="p-field p-col-12 p-md-12">
        <div class="p-grid p-jc-start p-md-1">
          <label for="content">Content</label>
        </div>
        <Editor
          v-model="snippetForm.content"
          id="content"
          editorStyle="height: 300px;"
          placeholder="Type code here"
        >
          <template #toolbar></template>
        </Editor>
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
export default {
  name: "SnippetEditor",
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
      },
      options: {
        programmingLanguages: [],
        folders: []
      }
    };
  },
  methods: {
    cancelEdit() {
      this.$emit("cancel-edit");
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
      return this.targetFolder;
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
