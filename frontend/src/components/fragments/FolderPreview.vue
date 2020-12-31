<template>
  <div v-if="!editModeEnabled">
    <div class="p-d-flex p-jc-between">
      <!-- folder label, snippet count and new snippet button -->
      <div class="p-flex-column">
        <div class="p-mb-1">
          <p style="margin-top: 0; font-size: 50px;">
            {{ selectedFolder.label }}
          </p>
        </div>
        <div class="p-mb-2" id="sub_header">{{ snippetCount }}</div>
      </div>
      <div>
        <Button
          label="New Snippet"
          icon="pi pi-plus"
          iconPos="left"
          class="p-button-outlined p-button-warning p-button-raised"
          id="new_snippet_btn"
          @click="enableEditModeNew()"
        >
        </Button>
      </div>
    </div>
    <!-- snippet list -->
    <DataTable
      id="snippet_list"
      :value="folderSnippets"
      v-model:selection="selectedSnippet"
      selectionMode="single"
      :scrollable="true"
      scrollHeight="675px"
      dataKey="id"
    >
      <Column class="p-text-capitalize" field="title" header="Title" />
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
              <Tag class="preview-tag p-mr-2 p-mb-2 p-mt-2 p-ml-1">{{
                tag
              }}</Tag>
            </template>
          </ScrollPanel>
        </template>
      </Column>
    </DataTable>
  </div>
  <div v-else>
    <!-- container to present form for editing and creating new snippets -->
    <SnippetEditor
      :edit-mode="editMode"
      :target-folder="selectedFolder"
      @close-edit="disableEditMode"
    />
  </div>
</template>

<script>
import { useQuery, useResult } from "@vue/apollo-composable";
import getSnippetsByFolderQuery from "@/graphql/queries/getSnippetsByFolder.query.graphql";
import SnippetEditor from "@/components/fragments/SnippetEditor";

export default {
  name: "FolderPreview",
  components: { SnippetEditor },
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
  mounted() {
    this.snippetList = this.folderSnippets;
  },
  updated() {
    this.$nextTick(() => {});
  },
  data() {
    return {
      selectedSnippet: null,
      editMode: {
        newSnippet: false,
        modifySnippet: false
      },
      snippetList: []
    };
  },
  watch: {
    selectedFolder() {
      this.disableEditMode();
    }
  },
  methods: {
    enableEditModeNew() {
      this.editMode.newSnippet = true;
      this.editMode.modifySnippet = false;
    },
    enableEditModeModify() {
      this.editMode.modifySnippet = true;
      this.editMode.newSnippet = false;
    },
    disableEditMode() {
      this.editMode.newSnippet = false;
      this.editMode.modifySnippet = false;
    }
  },
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
    },
    editModeEnabled() {
      return (
        this.editMode.newSnippet === true ||
        this.editMode.modifySnippet === true
      );
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
  padding: 0 20px 0 20px;
}
#tag_list {
  width: 100%;
  height: 45px;
}
#new_snippet_btn {
  margin-top: 15px;
  margin-right: 15px;
  font-weight: bold;
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
tr.p-selectable-row:active {
  background-color: #d3d4d6;
}
#snippet_list tr:hover {
  background-color: #6c757d !important;
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
.p-datatable-scrollable-header-box {
  padding-right: 0px !important;
}
.p-datatable-scrollable-body::-webkit-scrollbar {
  width: 5px !important;
}
.p-datatable-scrollable-body::-webkit-scrollbar-thumb {
  width: 4px !important;
  background-color: #6c757d;
    border-radius: 5px;
}
</style>
