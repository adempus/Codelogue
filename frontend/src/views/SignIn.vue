<template>
  <div class="p-grid p-justify-center">
    <div class="signin_section">
      <SignInForm></SignInForm>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SignIn',
  watch: {
    isSignedIn() {
      if (this.isSignedIn) {
        // this.$router.replace({ name: 'Home', params: { username: this.username } });
        this.$router.replace({ name: 'Home' });
      }
    }
  },
  computed: {
    isSignedIn() {
      return this.$store.getters.isSignedIn;
    }
  },
};
</script>

<style scoped>
  .signin_section {
    width: max-content !important;
    margin: 250px 700px 0 700px;
  }
  @media(max-width: 1450px) {
    .signin_section {
      width: max-content !important;
      margin: 200px 0 0 0;
    }
  }
  @media(max-width: 1024px) {
    .signin_section {
      width: max-content !important;
      margin: 200px 0 0 0;
    }
  }
</style>
