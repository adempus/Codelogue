<template>
  <div>
    <h2>Snippet</h2>
    <pre><code class="language-javascript">
          {{ snippetQueryResult }}
    </code></pre>
  </div>
</template>

<script>
import { useRoute } from "vue-router";
import { useQuery, useResult } from "@vue/apollo-composable";
import getSnippetById from "@/graphql/queries/getSnippetById.query.graphql";

export default {
  name: "SnippetPreview",
  data() {
    return {
      title: "",
      programmingLanguage: {},
      folder: {},
      description: "",
      dateCreated: "",
      tags: []
    };
  },
  setup() {
    const route = useRoute();
    const { result } = useQuery(getSnippetById, () => ({
      snippetId: route.params.id
    }));
    const snippetById = useResult(result, null, data => data["getSnippetById"]);
    return { snippetById };
  },
  computed: {
    snippetQueryResult() {
      if (this.snippetById === null) return;
      return this.snippetById;
    },
  }
};
</script>

<style scoped></style>
