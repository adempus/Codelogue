<template>
  <div>
    <Menubar class="navbar p-shadow-1" v-model="items">
      <template #start>
        <h1 class="app_name">codelogue_</h1>
      </template>
      <template #end>
        <div v-if="!isSignedIn">
          <Button type="button" class="p-button-sm login_btn" label="Sign In"
                  @click="navSignInPage()"/>
        </div>
        <div v-else class="p-grid">
          <Button icon="pi pi-power-off"
                  id="signout_btn"
                  class="p-col p-button-rounded p-button-outlined"/>
        </div>
      </template>
    </Menubar>
  </div>
</template>
<script>
export default {
  name: 'Navbar',
  mounted() {
    this.hideDefaultNavButton();
  },
  data() {
    return {
      items: [{ label: 'Username', icon: 'pi pi-power-off', visible: this.isSignedIn }],
    };
  },
  methods: {
    hideDefaultNavButton() {
      document.getElementsByClassName('p-menubar-button')[0].style.visibility = 'hidden';
    },
    navSignInPage() {
      this.$router.push('sign-in');
    },
  },
  computed: {
    isSignedIn() {
      return this.$store.getters.isSignedIn;
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
    background-color: #272A36;
    border-color: #272A36;
    z-index: 100;
  }
  .app_name {
    font-family: 'NTR', sans-serif;
    font-weight: 400;
    color: #DB564E;
  }
  .login_btn {
    background-color: #DB564E;
    border-color: #DB564E;
    display: inline-block;
    height: 35px;
  }


  #signout_btn {
    background-color: inherit;
    border-color: #DB564E;
    color: #DB564E;
    height: 40px;
    width: 40px;
  }
  #signout_btn:focus {
    outline: none;
    box-shadow: none;
  }
  #signout_btn:hover {
    background-color: #DB564E;
    color: #272A36;
  }
  #signout_btn:active {
    background-color: #e58883;
    border-color: #e58883;
    color: #272A36;
  }
</style>
