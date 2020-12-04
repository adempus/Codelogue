<template>
  <div v-if="!userSignedIn">
    <h4>Authorization Error</h4>
    <p class="base">You must be signed in to access.</p>
    <br />
    <router-link to="/sign-in" class="link">Click here to sign in</router-link>
  </div>
  <div v-else>
    <h1>Welcome {{ userInfo.username }}</h1>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  beforeMount() {
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
* {
  color: #ffffff;
}
.link {
  color: cornflowerblue;
}
</style>
