<template>
  <Navbar></Navbar>
  <router-view />
</template>
<script>
import Navbar from "@/components/Navbar.vue";

export default {
  components: { Navbar }
};
</script>
<style>
@import url("https://fonts.googleapis.com/css2?family=NTR&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Inconsolata:wght@500&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Open+Sans&display=swap");

body {
  padding-top: 10%;
}
body, html {
  height: 100%;
  background-color: #323645;
}
button:focus {
  outline: none !important;
  box-shadow: none !important;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif, NTR;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
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
