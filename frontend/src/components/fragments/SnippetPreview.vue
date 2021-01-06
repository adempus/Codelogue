<template>
  <div>
    <h2>Snippet</h2>
    {{ snippetQueryResult }}
  </div>
</template>

<script>
import { useQuery, useResult } from "@vue/apollo-composable";
import getSnippetById from "@/graphql/queries/getSnippetById.query.graphql";

export default {
  name: "SnippetPreview",
  setup(props) {
    const { result } = useQuery(getSnippetById, () => ({
      snippetId: props.snippetSelection.id
    }));
    const snippetById = useResult(result, null, data => data["getSnippetById"]);
    return { snippetById };
  },
  props: {
    snippetSelection: {
      required: true,
      type: Object
    }
  },
  data() {
    return {
      snippet: {}
    };
  },
  computed: {
    selectedSnippet() {
      return this.snippetSelection;
    },
    snippetQueryResult() {
      if (this.snippetById === null) return;
      return this.snippetById;
    },
    snippetId() {
      return this.snippetSelection.key;
    }
  }
};
</script>

<style scoped></style>
