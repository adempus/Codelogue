<template>
  <div>
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

    <!-- sign in menu pop-up button (mobile) -->
    <Button @click="toggleMobileSignIn"
            icon="pi pi-user" aria:haspopup="true" aria-controls="overlay_panel"
            id="mobile_signin_popup_btn" class="p-button-sm login_btn"/>

    <!-- mobile sign-in pop-up -->
    <div id="mobile_signin_div">
      <Dialog header="Sign In" id="signin_popup"
              :style="{width: '65vw', margin: '5px 10px 5px 10px'}"
              :visible.sync="displayMobileSignIn" :modal="true">
        <div class="p-fluid" id="mobile_signin_form">
          <div class="p-field p-grid separator">
            <!-- mobile email input -->
            <FeedbackTextInput
                :value="email"
                :field-payload="getInputFieldPayload(
                    'p-col', loginEmailFieldError, loginEmailFeedback, 'email', 'p-inputtext-sm')"
                @input="(emailInput) => {this.email = emailInput}"
                :state="validateState('email')"/>
          </div>

          <div class="p-field p-grid separator">
            <!-- mobile password input -->
            <FeedbackTextInput
                :value="password"
                :field-payload="getInputFieldPayload(
                  'p-col', loginPasswordFieldError, loginPasswordFeedback,
                  'Password', 'p-inputtext-sm', 'password')"
                @input="(passwordInput) => {this.password = passwordInput}"
                :state="validateState('password')"/>
          </div>
        </div>
        <!-- signin button -->
        <Button @click="signInUser()"
                type="button" label="Login" class="p-button-sm login_btn"/>
      </Dialog>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
import { required, email } from 'vuelidate/lib/validators';
import FeedbackTextInput from './subcomponents/FeedbackTextInput.vue';

const emailNotFound = (value, vm) => !vm.signInState.invalidEmail;
const incorrectPassword = (value, vm) => !vm.signInState.invalidPassword;

export default {
  name: 'SignInForm',
  components: { FeedbackTextInput },
  data() {
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
      displayMobileSignIn: false,
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
    toggleMobileSignIn() {
      this.displayMobileSignIn = !this.displayMobileSignIn;
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
  watch: {
    displayMobileSignIn(value) {
      if (!value) {
        Object.assign(this.$data, this.$options.data.apply(this));
      }
    },
  },
  computed: {
    loginEmailFeedback() {
      return !this.$v.email.email ? 'Email invalid' : 'Email required';
    },
    loginPasswordFeedback() {
      return 'Password required';
    },
    loginEmailFieldError() {
      return this.signInState.requested && (!this.$v.email.email || !this.$v.email.required);
    },
    loginPasswordFieldError() {
      return this.signInState.requested && !this.$v.password.required;
    },
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
  #mobile_signin_form input {
    border-radius: 5px;
    background-color: #323645;
    border-color: #323645;
    color: #FFFFFF;
    font-family: 'Open Sans', sans-serif;
  }
  .error_txt {
    color: #eb897e;
    font-size: 0.75rem;
    font-family: 'Open Sans', sans-serif;
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
    border-color: #eb897e !important;
  }
  .p-dialog-content {
    background-color: #272A36 !important;
    border-radius: 5px !important;
    padding: 10% 10% 10% 10% !important;
  }
  .p-dialog-header {
    background-color: #272A36 !important;
    color: #DB564E !important;
    border-color: #272A36 !important;
    text-align: center !important;
    border-radius: 5px !important;
    font-family: 'Open Sans', sans-serif;
    letter-spacing: 1px;
  }
</style>

<style scoped>
  .login_btn {
    background-color: #DB564E;
    border-color: #DB564E;
    display: inline-block;
    height: 35px;
  }
  #mobile_signin_popup_btn {
    background-color: #323645;
    color: #DB564E;
    padding: 4px 0 0 0;
    width: 40px;
    height: 40px;
  }
  @media(max-width: 890px) {
    #signin_form {
      display: none;
    }
  }
  @media(min-width: 891px) {
    #mobile_signin_popup_btn {
      display: none;
    }
    #mobile_signin_form {
      display: none;
    }
    #mobile_signin_div {
      display: none;
    }
  }
  .separator {
    margin-bottom: 30px;
  }
</style>
