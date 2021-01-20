<template>
  <div v-if="!userSignedIn" class="top_placement" style="padding-top: 100px;">
    <h4>Authorization Error</h4>
    <p class="base">You must be signed in to access.</p>
    <br />
    <router-link to="/sign-in" class="link">Click here to sign in</router-link>
  </div>
  <div v-else>
    <div class="p-grid p-ai-stretch vertical-container dashboard">
      <div class="p-col-3">
        <div class="box box-stretched">
          <FolderPane />
        </div>
      </div>
      <div class="p-col-9">
        <div class="box box-stretched">
          <PreviewPane />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FolderPane from "@/components/fragments/FolderPane";
import PreviewPane from "@/components/fragments/PreviewPane";

export default {
  name: "Dashboard",
  components: { FolderPane, PreviewPane },
  mounted() {
    this.setAccessToken();
    this.$store.dispatch("checkUserAuthorization");
  },
  data() {
    return {};
  },
  methods: {
    setAccessToken() {
      if (localStorage.getItem("accessToken") !== null) {
        this.$store.dispatch("storeAccessToken");
      }
    }
  },
  computed: {
    getAccessToken() {
      return this.$store.getters.getAccessToken;
    },
    userInfo() {
      return this.$store.getters.getUserInfo;
    },
    userSignedIn() {
      if (this.$store.getters.authorizationState === null) return false;
      return !this.$store.getters.authorizationState.error;
    }
  }
};
</script>

<style scoped>
body,
html {
  overflow-y: hidden !important;
}
* {
  color: #ffffff;
}
.link {
  color: cornflowerblue;
}
.dashboard {
  margin-top: 60px;
  padding: 0 2px 0px 2px;
}
</style>
