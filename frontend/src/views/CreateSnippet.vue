<template style="overflow-x: hidden">
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
        @click="cancel"
      />
    </div>
  </div>
  <SnippetForm
    :folders-query-result="folderOptions"
    :languages-query-result="languageOptions"
    :default-folder="defaultFolder"
    :default-language="defaultLanguage"
  />
</template>

<script>
// import { useRoute } from "vue-router";
import { useQuery, useResult } from "@vue/apollo-composable";
import folderAndLanguageOptions from "@/graphql/queries/folderAndLanguageOptions.query.graphql";
// import getFolderById from "@/graphql/queries/getFolderById.query.graphql";
import SnippetForm from "@/components/fragments/SnippetForm";

export default {
  name: "CreateSnippet",
  components: { SnippetForm },
  setup() {
    // const route = useRoute();
    const fetchPolicy = { fetchPolicy: "network-only" };
    let { result } = useQuery(folderAndLanguageOptions, fetchPolicy);
    let folderQueryResult = useResult(
      result,
      null,
      data => data["getUserFolders"]
    );
    let languageQueryResult = useResult(
      result,
      null,
      data => data["allLanguages"]["edges"]
    );
    return { folderQueryResult, languageQueryResult };
  },
  methods: {
    cancel() {
      this.$router.go(-1);
    }
  },
  computed: {
    defaultFolder() {
      if (this.folderOptions.length <= 0) return [];
      return this.folderOptions.find(
        folder => folder["id"] === this.$route.params.folderId
      );
    },
    defaultLanguage() {
      if (this.languageOptions.length <= 0) return [];
      return this.languageOptions.find(
        lang => lang["name"].toLowerCase() === "plaintext"
      );
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
#title,
#folder,
#language {
  border-width: 2px;
  background-color: #313645;
}
</style>
