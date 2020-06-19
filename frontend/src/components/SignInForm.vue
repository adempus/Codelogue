<template>
  <div class="p-formgroup-inline" id="signin_form">
    <!-- email input -->
    <FeedbackTextInput
        :value="email"
        :field-payload="getInputFieldPayload(
          'p-field p-fluid', loginEmailFieldError, loginEmailFeedback, 'email', 'p-inputtext-sm')"
        @input="(emailInput) => {this.email = emailInput}"
        :state="validateState('email')"/>

    <!-- password input -->
    <FeedbackTextInput
        :value="password"
        :field-payload="getInputFieldPayload(
          'p-field p-fluid', loginPasswordFieldError, loginPasswordFeedback,
          'Password', 'p-inputtext-sm', 'password')"
        @input="(passwordInput) => {this.password = passwordInput}"
        :state="validateState('password')"/>

    <!-- signin button -->
    <Button @click="signInUser()"
            type="button" label="Login" class="p-button-sm login_btn"/>
  </div>
</template>
<script>
import axios from 'axios';
import { required, email } from 'vuelidate/lib/validators';
import FeedbackTextInput from './fragments/FeedbackTextInput.vue';

const emailNotFound = (value, vm) => !vm.signInState.invalidEmail;
const incorrectPassword = (value, vm) => !vm.signInState.invalidPassword;

export default {
  name: 'SignInForm',
  components: { FeedbackTextInput },
  data: () => {
    return {
      email: '',
      password: '',
      signInState: {
        requested: false,
        invalidEmail: false,
        invalidPassword: false,
        attemptedEmail: '',
        attemptedPassword: '',
      },
      response: {},
    };
  },
  validations: {
    email: {
      required,
      email,
      emailNotFound
    },
    password: {
      required,
      incorrectPassword
    },
  },
  methods: {
    validateState(value) {
      const { $dirty, $error } = this.$v[value];
      return $dirty ? !$error : null;
    },
    signInUser() {
      this.$set(this.signInState, 'requested', true);
      this.$v.$touch();

      if (this.$v.$invalid) {
        console.log('Invalid sign in credentials provided');
        console.log('Error list: ');
        console.log('email required error:  ', !this.$v.email.required);
        console.log('email format error:  ', !this.$v.email.email);
        console.log('password required error: ', !this.$v.password.required);
      } else {
        console.log('Valid sign in credentials provided');
        console.log('email required error:  ', !this.$v.email.required);
        console.log('email format error:  ', !this.$v.email.email);
        console.log('password required error: ', !this.$v.password.required);
      }
    },
    requestSignIn() {
      const endpoint = this.$root.signIn;
      return axios.post(endpoint, {
        email: this.email,
        password: this.password
      });
    },
  },
  computed: {
    loginEmailFeedback() {
      return !this.$v.email.email ? 'Email is invalid' : 'Email is required';
    },
    loginPasswordFeedback() {
      return 'Password is required';
    },
    loginEmailFieldError() {
      return this.signInState.requested && (!this.$v.email.email || !this.$v.email.required);
    },
    loginPasswordFieldError() {
      return this.signInState.requested && !this.$v.password.required;
    }
  }
};
</script>
<style>
  #signin_form input {
    border-radius: 5px;
    background-color: #323645;
    border-color: #323645;
    color: #FFFFFF;
    font-family: 'Open Sans', sans-serif;
  }

  .error_txt {
    color: #E46052;
    font-size: 0.75rem;
  }

  .email_error_div {
    margin-bottom: -100%;
    margin-right: 45%;
  }

  .password_error_div {
    margin-bottom: -100%;
    margin-right: 30%;
  }

  .p-invalid {
    border-color: #E46052 !important;
  }

</style>

<style scoped>
  .login_btn {
    background-color: #DB564E;
    border-color: #db564e;
    display: inline-block;
    height: 35px;
  }

  @media(max-width: 960px) {
    #signin_form {
      visibility: hidden;
    }
  }
</style>
