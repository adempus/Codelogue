<template>
  <div class="p-d-flex p-jc-between">
    <div class="p-flex-column">
      <!-- folder label and count -->
      <div class="p-mb-2">
        <p style="margin-top: 0; font-size: 50px;">
          {{ selectedFolder.label }}
        </p>
      </div>
      <div class="p-mb-2" id="sub_header">{{ snippetCount }}</div>
    </div>
    <div>
      <Button class="p-button-warning p-button-raised">
        <b style="color: #323645">New Snippet</b>
      </Button>
    </div>
  </div>
  <!-- snippet list -->
  <DataTable
    id="snippet_list"
    :value="folderSnippets"
    v-model:selection="selectedSnippet"
    selectionMode="single"
    dataKey="id"
  >
    <Column field="title" header="Title" />
    <Column field="programmingLanguage" header="Programming Language">
      <template #body="slotProps">
        <Tag :value="slotProps.data.programmingLanguage" />
      </template>
    </Column>
    <Column field="created" header="Created" />
    <Column field="tags" header="Tags">
      <template #body="tagProps">
        <ScrollPanel id="tag_list">
          <template v-for="tag in tagProps.data.tags" v-bind:key="tag">
            <Tag class="preview-tag p-mr-2 p-mb-2 p-mt-2 p-ml-1">{{ tag }}</Tag>
          </template>
        </ScrollPanel>
      </template>
    </Column>
  </DataTable>
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
  props: {
    folderSelection: {
      required: true,
      type: Object
    }
  },
  data() {
    return {
      selectedSnippet: null
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
          programmingLanguage: snippet["ProgrammingLanguage"]["name"],
          tags: snippet["tags"]["edges"].map(tag => {
            return tag["node"]["keyword"];
          })
        };
      });
    },
    snippetCount() {
      const length = this.selectedFolder.children.length;
      return `${length} ${length === 1 ? "snippet" : "snippets"}`;
    }
  }
};
</script>

<style scoped>
#sub_header {
  position: fixed;
  margin-top: -50px;
  padding-left: 5px;
  color: #6c757d;
  font-size: 20px;
}
#snippet_list {
  border-left: #6c757d;
}
#tag_list {
  width: 100%;
  height: 45px;
}
.preview-tag {
  background-color: #61667b;
}
</style>
<style>
#snippet_list.p-datatable .p-datatable-thead > tr > th {
  background-color: #272a36 !important;
  color: #ffffff !important;
  border-color: #61667b;
}
#snippet_list.p-datatable .p-datatable-tbody > tr > td {
  background-color: #272a36;
  color: #ffffff;
  border-color: #454a5e;
}

#tag_list.p-scrollpanel .p-scrollpanel-content {
  background-color: #272a36 !important;
  overflow-x: scroll;
  overflow-y: hidden;
  white-space: nowrap;
  width: 100%;
}

#tag_list.p-scrollpanel .p-scrollpanel-bar-x {
  height: 2px;
  background-color: #454a5e;
}
#tag_list.p-scrollpanel .p-scrollpanel-bar-y {
  visibility: hidden;
}
</style>
