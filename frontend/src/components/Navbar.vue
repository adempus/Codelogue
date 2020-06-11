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
  data: () => {
    return {
      items: [],

    };
  },
};
</script>

<style scoped>
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 70px;
    padding-left: 4vw;
    padding-right: 8vw;
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
</style>
