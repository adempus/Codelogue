<template>
  <div v-if="!userSignedIn">
    <h4>Authorization Error</h4>
    <p class="base">You must be signed in to access.</p>
    <br />
    <router-link to="/sign-in" class="link">Click here to sign in</router-link>
  </div>
  <div v-else>
    <h1>Welcome {{ user.username }}</h1>
    <p >{{ authResponse }}</p>
  </div>
</template>

<script>
import { useMutation } from "@vue/apollo-composable";
import checkAuthorizationMutation from "../graphql/mutations/checkAuthorization.mutation.graphql";

export default {
  name: "Dashboard",
  setup() {
    const { mutate: checkAuthorization } = useMutation(
      checkAuthorizationMutation
    );
    return { checkAuthorization };
  },
  beforeMount() {
    this.setAccessToken();
  },
  mounted() {
    this.$nextTick(() => {
      this.checkUserAuthorization();
    });
  },
  data() {
    return {
      authResponse: null,
      user: null
    };
  },
  methods: {
    checkUserAuthorization() {
      const token = this.getAccessToken;
      console.log("token: ", token);
      this.checkAuthorization()
        .then(res => (this.authResponse = res["data"]["checkAuthorization"]))
        .catch(err => console.log("An error occurred", err))
        .finally(() => {
          if (this.userSignedIn) this.user = this.authResponse.user;
        });
    },
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
    userSignedIn() {
      if (this.authResponse === null) return false;
      return !this.authResponse.error;
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
