<template>
  <div style="color: #ffffff;">Count: {{ getCount }}</div>
  <div class="p-d-flex p-flex-column">
    <div class="p-mb-2">
      <Button
        label="Increment"
        class="p-button-success"
        v-on:click="incrementCount"
      />
    </div>
    <div class="p-mb-2">
      <Button
        label="Decrement"
        class="p-button-danger"
        v-on:click="decrementCount"
      />
    </div>
  </div>
</template>

<script>
import { useQuery } from "@vue/apollo-composable";
import allLanguagesQuery from "../graphql/queries/allLanguages.query.graphql";

export default {
  name: "Counter",
  mounted() {
    const { result } = useQuery(allLanguagesQuery);
    this.results = result;
  },
  data() {
    return {
      results: null
    };
  },
  // setup() {
  //   const { result } = useQuery(allLanguagesQuery);
  //   return result;
  // },
  methods: {
    incrementCount() {
      this.$store.dispatch("increment");
      console.log(this.result);
    },
    decrementCount() {
      this.$store.dispatch("decrement");
    }
  },
  computed: {
    getCount() {
      return this.$store.state.count;
    }
  }
};
</script>

<style scoped></style>
