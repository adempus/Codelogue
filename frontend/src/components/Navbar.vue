<template>
  <div>
    <Menubar class="navbar p-shadow-1" v-model="items">
      <template #start>
        <h1 class="app_name">codelog_</h1>
      </template>
      <template #end>
        <div v-if="!isSignedIn">
          <Button
            type="button"
            class="p-button-sm login_btn"
            label="Sign In"
            @click="navSignInPage"
          />
        </div>
        <div v-else class="p-grid">
          <Button
            icon="pi pi-power-off"
            id="signout_btn"
            class="p-col p-button-rounded p-button-outlined"
            @click="signOut"
          />
        </div>
      </template>
    </Menubar>
  </div>
</template>
<script>
export default {
  name: "Navbar",
  mounted() {
    this.hideDefaultNavButton();
  },

  data() {
    return {
      items: [
        { label: "Username", icon: "pi pi-power-off", visible: this.isSignedIn }
      ]
    };
  },
  methods: {
    hideDefaultNavButton() {
      document.getElementsByClassName("p-menubar-button")[0].style.visibility =
        "hidden";
    },
    navSignInPage() {
      this.$router.push("sign-in");
    },
    signOut() {
      localStorage.clear();
      window.location.pathname = "/sign-in";
    }
  },
  computed: {
    isSignedIn() {
      if (this.$store.getters.authorizationState === null) return false;
      return !this.$store.getters.authorizationState.error;
    }
  }
};
</script>
<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 83px;
  padding-left: 4vw;
  padding-right: 4vw;
  background-color: #272a36;
  border-color: #272a36;
  z-index: 100;
}
.app_name {
  font-family: "NTR", sans-serif;
  font-weight: 400;
  color: #db564e;
}
.login_btn {
  background-color: #db564e;
  border-color: #db564e;
  display: inline-block;
  height: 35px;
}

#signout_btn {
  background-color: inherit;
  border-color: #db564e;
  color: #db564e;
  height: 40px;
  width: 40px;
}
#signout_btn:focus {
  outline: none;
  box-shadow: none;
}
#signout_btn:hover {
  background-color: #db564e;
  color: #272a36;
}
#signout_btn:active {
  background-color: #e58883;
  border-color: #e58883;
  color: #272a36;
}
</style>
