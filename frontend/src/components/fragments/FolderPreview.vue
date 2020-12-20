<template>
  <div>
    <h2>Folder</h2>
    {{ folderSnippets }}
    <!--    {{ parseSnippetsByFolderResponse() }}-->
    <!--    {{ parse() }}-->
  </div>
</template>

<script>
import { useQuery, useResult } from "@vue/apollo-composable";
import getSnippetsByFolderQuery from "@/graphql/queries/getSnippetsByFolder.query.graphql";

export default {
  name: "FolderPreview",
  setup(props) {
    const { result } = useQuery(getSnippetsByFolderQuery, () => ({
      folderId: props.folderSelection.key
    }));
    const snippetsByFolder = useResult(
      result,
      null,
      data => data["getSnippetsByFolder"]
    );
    return { snippetsByFolder };
  },
  mounted() {
    this.$nextTick(() => {
      // this.snippetsByFolderQueryResponse = this.snippetsByFolder();
    });
  },
  props: {
    folderSelection: {
      required: true,
      type: Object
    }
  },
  data() {
    return {
      snippetsByFolderQueryResponse: null
    };
  },
  methods: {},
  computed: {
    selectedFolder() {
      return this.folderSelection;
    },
    folderId() {
      return this.folderSelection.key;
    },
    folderSnippets() {
      if (this.snippetsByFolder === null) return;
      return this.snippetsByFolder.map(snippet => {
        return {
          id: snippet["id"],
          title: snippet["title"],
          created: snippet["dateCreated"],
          tags: snippet["tags"]["edges"].map(tag => {
            return {
              keyword: tag["node"]["keyword"]
            };
          })
        };
      });
    }
  }
};
</script>

<style scoped></style>
