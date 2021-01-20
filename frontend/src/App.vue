<template>
  <div class="p-grid p-flex-column">
    <div class="p-col">
      <Navbar></Navbar>
    </div>
    <div class="p-col">
      <Dashboard v-show="userSignedIn" />
    </div>
    <router-view name="Index" />
  </div>
</template>
<script>
import Navbar from "@/components/Navbar.vue";
import Dashboard from "@/views/Dashboard";

export default {
  components: { Navbar, Dashboard },
  setup() {
    const g = () => {
      if (this.$store.getters.authorizationState === null) return false;
      return !this.$store.getters.authorizationState.error;
    };
    return { g };
  },
  computed: {
    userSignedIn() {
      if (this.$store.getters.authorizationState === null) return false;
      return !this.$store.getters.authorizationState.error;
    }
  }
};
</script>
<style>
@import url("https://fonts.googleapis.com/css2?family=NTR&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Inconsolata:wght@500&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Open+Sans&display=swap");

body,
html {
  height: 100%;
  background-color: #323645;
  overflow-y: hidden;
  padding-bottom: 17px;
}
.top_placement {
  margin-top: 83px !important;
}
button:focus {
  outline: none !important;
  box-shadow: none !important;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif, NTR;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-y: hidden;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}
#nav a.router-link-exact-active {
  color: #42b983;
}
#app {
  margin-left: 0;
  overflow-x: hidden;
}
</style>
