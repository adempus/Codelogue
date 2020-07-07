<template>
  <Card id="signin_card">
    <template slot="title">
      <h1 id="signin_header">Sign In</h1>
    </template>
    <template slot="content">
      <form class="p-fluid p-formgrid p-grid p-justify-center">
        <!-- email input -->
        <FeedbackTextInput
            :value="email"
            :field-payload="getInputFieldPayload(
                    'p-field p-col-12', loginEmailFieldError, loginEmailFeedback,
                    'email', 'p-inputtext-sm')"
            @input="(emailInput) => {this.email = emailInput}"
            :state="validateState('email')"/>
        <!-- password input -->
        <FeedbackTextInput
            :value="password"
            :field-payload="getInputFieldPayload(
                  'p-field p-col-12 ', loginPasswordFieldError, loginPasswordFeedback,
                  'Password', 'p-inputtext-sm', 'password')"
            @input="(passwordInput) => {this.password = passwordInput}"
            :state="validateState('password')"/>

        <!-- sign-in button -->
        <Button @click="signInUser()"
                type="button" label="Login" class="p-button-sm login_btn" id="signin_btn"/>
      </form>
      <p class="success_msg" v-show="signInStatus.successful">Success</p>
    </template>
  </Card>
</template>
<script>
import axios from 'axios';
import { required, email } from 'vuelidate/lib/validators';
import FeedbackTextInput from './subcomponents/FeedbackTextInput.vue';

const emailNotFound = (value, vm) => !vm.signInStatus.isNonexistentEmail
  && (value.toUpperCase() !== vm.signInStatus.attemptedEmail.toUpperCase());
const incorrectPassword = (value, vm) => !vm.signInStatus.isWrongPassword
  && value !== vm.signInStatus.attemptedPassword;

export default {
  name: 'SignInForm',
  components: { FeedbackTextInput },
  data() {
    return {
      email: '',
      password: '',
      signInStatus: {
        submitClicked: false,
        response: null,
        isNonexistentEmail: false,
        isWrongPassword: false,
        attemptedEmail: '',
        attemptedPassword: '',
        successful: false,
      },
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
      this.$set(this.signInStatus, 'submitClicked', true);
      this.$v.$touch();

      if (this.$v.$invalid) {
        console.log('Invalid sign in credentials provided');
        return;
      }
      this.requestSignIn().then((response) => {
        console.log('sign in response: ', response);
        this.$set(this.signInStatus, 'response', response.data);
        if (this.signInStatus.response.error) {
          console.log('error occured');
          this.$set(this.signInStatus, 'successful', false);
          this.$set(
            this.signInStatus,
            'isNonexistentEmail',
            this.signInStatus.response.message.userNotFound
          );
          this.$set(
            this.signInStatus,
            'isWrongPassword',
            this.signInStatus.response.message.passwordInvalid
          );
          this.trackResponseErrors();
        } else {
          this.$set(this.signInStatus, 'successful', true);
        }
      });
    },
    requestSignIn() {
      const endpoint = this.$root.signIn;
      return axios.post(endpoint, {
        email: this.email,
        password: this.password
      });
    },
    trackResponseErrors() {
      if (this.signInStatus.isNonexistentEmail) {
        this.$set(this.signInStatus, 'attemptedEmail', this.email);
      }
      if (this.signInStatus.isWrongPassword) {
        this.$set(this.signInStatus, 'attemptedPassword', this.password);
      }
    },
    applyFieldChange(signInStatusErrorObj, errorObjName, condition) {
      if (this.signInStatus.response !== null) {
        if (this.signInStatus.submitClicked && this.signInStatus.response.error) {
          if (signInStatusErrorObj) this.$set(this.signInStatus, errorObjName, condition);
        }
      }
    }
  },
  watch: {
    email() {
      this.applyFieldChange(
        this.signInStatus.isNonexistentEmail,
        'isNonexistentEmail',
        this.signInStatus.attemptedEmail.toUpperCase() === this.email.toUpperCase()
      );
    },
    password() {
      this.applyFieldChange(
        this.signInStatus.isWrongPassword,
        'isWrongPassword',
        this.signInStatus.attemptedPassword === this.password
      );
    },
    displayMobileSignIn(value) {
      if (!value) {
        Object.assign(this.$data, this.$options.data.apply(this));
      }
    },
  },
  computed: {
    loginEmailFieldError() {
      return this.signInStatus.submitClicked
        && (!this.$v.email.email || !this.$v.email.required || !this.$v.email.emailNotFound);
    },
    loginEmailFeedback() {
      if (!this.$v.email.required) return 'Email required';
      return !this.$v.email.emailNotFound ? 'This email is not registered. Try again.'
        : 'Email invalid';
    },
    loginPasswordFieldError() {
      return this.signInStatus.submitClicked
        && (!this.$v.password.required || !this.$v.password.incorrectPassword);
    },
    loginPasswordFeedback() {
      return !this.$v.password.incorrectPassword ? 'Incorrect password. Try again.'
        : 'Password required';
    },
  }
};
</script>
<style>
  #signin_card {
    width: max-content;
    background-color: #272a36;
    border-radius: 5px;
    padding: 0 30px 10px 30px;
  }
  #signin_card input {
    border-radius: 5px;
    background-color: #323645;
    border-color: #323645;
    color: #FFFFFF;
    font-family: 'Open Sans', sans-serif;
    margin-top: 15px;
  }
  #signin_btn {
    background-color: #DB564E;
    border-color: #DB564E;
    width: 100px;
    margin-top: 25px;
    font-family: 'Open Sans', sans-serif;
  }
  #signin_header {
    color: #DB564E;
    font-family: 'NTR', sans-serif;
    margin: 0 0 -35px 0;
    text-align: left;
    font-weight: 500;
  }
  .error_txt {
    color: #eb897e;
    font-size: 0.75rem;
    font-family: 'Open Sans', sans-serif;
  }
  .p-invalid {
    border-color: #eb897e !important;
  }
  .success_msg {
    color: #00CD6F;
    font-size: 13px;
    padding-top: 5px;
    text-align: right;
  }
</style>

<style scoped>
  .login_btn {
    background-color: #DB564E;
    border-color: #DB564E;
    display: inline-block;
    margin-top: 12px;
    height: 35px;
  }

  .separator {
    margin-bottom: 30px;
  }

</style>
