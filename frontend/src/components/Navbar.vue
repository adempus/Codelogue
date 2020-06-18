<template>
  <div>
    <Menubar class="navbar p-shadow-1" v-model="items">
      <template #start>
        <h1 class="app_name">codelogue_</h1>
      </template>
      <template #end>
        <SignInForm></SignInForm>
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
      items: [],
    };
  },
  methods: {
    hideDefaultNavButton() {
      document.getElementsByClassName('p-menubar-button')[0].style.visibility = 'hidden';
    }
  },
};
</script>

<style scoped>
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 80px;
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
</style>
