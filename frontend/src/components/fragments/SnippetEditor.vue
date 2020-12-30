<!--
This component contains a separate form component for creating and editing snippets, and makes queries for data
to be passed into the form component depending on whether edit mode is "new" or "modify".
 -->
<template style="overflow-x: hidden">
  <div v-if="editModeNew">
    <div class="p-d-flex p-jc-between">
      <div class="p-flex-column">
        <div class="p-mb-2">
          <!-- Header -->
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
          @click="closeEdit"
        />
      </div>
    </div>
    <!-- new snippet form -->
    <SnippetForm
      :folders-query-result="foldersQueryResult"
      :languages-query-result="languagesQueryResult"
      :default-folder="selectedFolder"
      :default-language="selectedLanguage"
      @new-submission-complete="closeEdit"
    />
  </div>
  <div v-else-if="editModeModify">
    <h1>Modify Snippet</h1>
  </div>
</template>

<script>
import { useQuery, useResult } from "@vue/apollo-composable";
import folderAndLanguageOptions from "@/graphql/queries/folderAndLanguageOptions.query.graphql";
import SnippetForm from "@/components/fragments/SnippetForm";

export default {
  name: "SnippetEditor",
  components: { SnippetForm },
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
  methods: {
    closeEdit() {
      this.$emit("close-edit");
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
    foldersQueryResult() {
      if (this.folderQueryResult === null) return [];
      return this.folderQueryResult;
    },
    selectedLanguage() {
      if (this.languagesQueryResult.length <= 0) return [];
      return this.languagesQueryResult.find(
        lang => lang["name"].toLowerCase() === "plaintext"
      );
    },
    languagesQueryResult() {
      if (this.languageQueryResult === null) return [];
      return this.languageQueryResult.map(lang => {
        return {
          id: lang["node"]["id"],
          name: lang["node"]["name"]
        };
      });
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
