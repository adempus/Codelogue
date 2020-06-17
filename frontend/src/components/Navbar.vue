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
    console.log('Mounted navbar.');
  },
  nextTick() {
    this.adjustSignInDrawerPosition();
  },
  data() {
    return {
      items: [],

    };
  },
  methods: {
    adjustSignInDrawerPosition() {
      let menubar = document.getElementsByClassName('.p-menubar-button');
      console.log('Menubar: ', menubar);
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

  .navbar .p-menubar-button {
        display: flex;
        position: relative;
        left: 95%;
  }
  /*.navbar .p-menubar .p-menubar-button {*/
  /*  display: flex;*/
  /*  color: #6c757d;*/
  /*  background: transparent;*/
  /*  border: 1px solid #dee2e6;*/
  /*  width: 2.5rem;*/
  /*  height: 2.5rem;*/
  /*  border-radius: 3px;*/
  /*  transition: box-shadow 0.2s;*/
  /*  position: absolute !important;*/
  /*  right: 10px !important;*/
  /*}*/


  @media screen and (max-width: 960px) {
    .navbar .p-menubar .p-menubar-button {
      display: flex;
      color: #6c757d;
      background: transparent;
      border: 1px solid #dee2e6;
      width: 2.5rem;
      height: 2.5rem;
      border-radius: 3px;
      transition: box-shadow 0.2s;
      position: absolute !important;
      right: 10px !important;
    }
  }
</style>
