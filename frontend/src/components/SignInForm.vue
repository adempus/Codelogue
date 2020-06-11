<template>
  <div class="p-formgroup-inline">
    <div class="p-field">
      <InputText v-model="email"
                 type="email" placeholder="Email" class="p-inputtext-sm login_txtbox" />
    </div>
    <div class="p-field">
      <InputText v-model="password"
                 type="password" placeholder="Password" class="p-inputtext-sm login_txtbox"  />
    </div>
    <Button v-on:click="signIn()"
            type="button" label="Login" class="p-button-sm login_btn"/>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SignInForm',
  data: () => {
    return {
      email: '',
      password: '',
      response: {},
    };
  },
  methods: {
    signIn() {
      this.requestSignIn().then((response) => {
        console.log('response from server: ', response);
      });
    },
    requestSignIn() {
      const endpoint = this.$root.signIn;
      return axios.post(endpoint, {
        email: this.email,
        password: this.password
      });
    }
  },
};
</script>

<style scoped>
  .login_txtbox {
    width: 8.5vw;
  }

  .login_btn {
    background-color: #DB564E;
    border-color: #db564e;
  }
</style>
