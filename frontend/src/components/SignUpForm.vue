<template>
  <Card id="signup_card">
    <template slot="content">
      <form class="p-fluid p-formgrid p-grid p-justify-center">
        <!-- first name input -->
        <FeedbackTextInput
            :value="firstName"
            :field-payload="getInputFieldPayload(
              'p-field p-col-6', firstNameFieldError, 'First name required', 'First Name')"
            :state="validateState('firstName')"
            @input="(fNameInput) => { this.firstName = fNameInput }"/>

        <!-- last name input -->
        <FeedbackTextInput
            :value="lastName"
            :field-payload="getInputFieldPayload(
              'p-field p-col-6', lastNameFieldError, 'Last name required', 'Last Name')"
            :state="validateState('lastName')"
            @input="(lNameInput) => { this.lastName = lNameInput }"/>

        <!-- username input -->
        <FeedbackTextInput
            :value="username"
            :field-payload="getInputFieldPayload(
              'p-field p-col-12', usernameFieldError, usernameFieldFeedback, 'Username')"
            :state="validateState('username')"
            @input="(usernameInput) => { this.username = usernameInput }"/>

        <!-- email input -->
        <FeedbackTextInput
            :value="email"
            :field-payload="getInputFieldPayload(
              'p-field p-col-12', emailFieldError, emailFieldFeedback,
              'Email Address', inputType='email')"
            :state="validateState('email')"
            @input="(emailInput) => { this.email = emailInput }"/>

        <!-- password input -->
        <FeedbackTextInput
            :value="password"
            :field-payload="getInputFieldPayload(
              'p-field p-col-6', passwordFieldError, passwordFieldFeedback,
              'Password', size='', inputType='password')"
            :state="validateState('password')"
            @input="(passwordInput) => { this.password = passwordInput }"/>

        <!-- password confirmation -->
        <FeedbackTextInput
            :value="confirmPass"
            :field-payload="getInputFieldPayload(
              'p-field p-col-6', passwordFieldError, passwordMatchFeedback,
              'Confirm Password', size='', inputType='password')"
            :state="validateState('confirmPass')"
            @input="(confirmPassInput) => { this.confirmPass = confirmPassInput }"/>

        <!-- submit button -->
        <Button @click="submit()"
                type="button" label="Sign Up" class="p-button-sm " id="signup_btn"/>
      </form>
      <p class="success_msg" v-show="signUpStatus.successful">Success</p>
    </template>
  </Card>
</template>

<script>

import axios from 'axios';
import { required, minLength, sameAs, email } from 'vuelidate/lib/validators';

const emailUnique = (value, vm) => !vm.signUpStatus.isExistingEmail
  && (value.toUpperCase() !== vm.signUpStatus.attemptedEmail.toUpperCase());
const usernameUnique = (value, vm) => !vm.signUpStatus.isExistingUsername
  && value.toUpperCase() !== vm.signUpStatus.attemptedUsername.toUpperCase();

export default {
  name: 'SignUpForm',
  data: () => {
    return {
      firstName: '',
      lastName: '',
      username: '',
      email: '',
      password: '',
      confirmPass: '',
      signUpStatus: {
        submitClicked: false,
        response: null,
        isExistingEmail: false,
        isExistingUsername: false,
        attemptedUsername: '',
        attemptedEmail: '',
        successful: false
      },
    };
  },
  validations: {
    firstName: {
      required
    },
    lastName: {
      required
    },
    username: {
      required,
      minLength: minLength(3),
      usernameUnique,
    },
    email: {
      required,
      email,
      emailUnique,
    },
    password: {
      required,
      minLength: minLength(7)
    },
    confirmPass: {
      required,
      sameAsPassword: sameAs('password')
    }
  },
  methods: {
    validateState(value) {
      const { $dirty, $error } = this.$v[value];
      return $dirty ? !$error : null;
    },
    submit() {
      this.$set(this.signUpStatus, 'submitClicked', true);
      this.$v.$touch();

      if (this.$v.$invalid) {
        console.log('Invalid credentials provided.');
        return;
      }
      this.requestSignUp().then((response) => {
        console.log('sign up response: ', response);
        this.$set(this.signUpStatus, 'response', response.data);
        if (this.signUpStatus.response.error) {
          console.log('error occured');
          this.$set(this.signUpStatus, 'successful', false);
          this.$set(
            this.signUpStatus,
            'isExistingEmail',
            this.signUpStatus.response.message.emailExists
          );
          this.$set(
            this.signUpStatus,
            'isExistingUsername',
            this.signUpStatus.response.message.usernameExists
          );
          this.trackResponseErrors();
        } else {
          this.$set(this.signUpStatus, 'successful', true);
        }
      });
    },
    requestSignUp() {
      const endpoint = this.$root.signUp;
      return axios.post(endpoint, {
        firstName: this.firstName,
        lastName: this.lastName,
        username: this.username,
        email: this.email,
        password: this.password
      });
    },
    trackResponseErrors() {
      if (this.signUpStatus.isExistingUsername) {
        this.$set(this.signUpStatus, 'attemptedUsername', this.username);
      }
      if (this.signUpStatus.isExistingEmail) {
        this.$set(this.signUpStatus, 'attemptedEmail', this.email);
      }
    },
    /**
     * To clear username and email field error messages after corrections are made to them,
     * post server side validation.
     * */
    applyFieldChange(signUpStatusErrorObj, errorObjName, condition) {
      if (this.signUpStatus.response !== null) {
        if (this.signUpStatus.submitClicked && this.signUpStatus.response.error) {
          if (signUpStatusErrorObj) this.$set(this.signUpStatus, errorObjName, condition);
        }
      }
    }
  },
  watch: {
    email() {
      this.applyFieldChange(
        this.signUpStatus.isExistingEmail,
        'isExistingEmail',
        this.signUpStatus.attemptedEmail.toUpperCase() === this.email.toUpperCase()
      );
    },
    username() {
      this.applyFieldChange(
        this.signUpStatus.isExistingUsername,
        'isExistingUsername',
        this.signUpStatus.attemptedUsername.toUpperCase() === this.username.toUpperCase()
      );
    },
  },
  computed: {
    firstNameFieldError() {
      return this.signUpStatus.submitClicked && !this.$v.firstName.required;
    },
    lastNameFieldError() {
      return this.signUpStatus.submitClicked && !this.$v.lastName.required;
    },
    usernameFieldError() {
      return this.signUpStatus.submitClicked
        && (!this.$v.username.required || !this.$v.username.minLength
          || !this.$v.username.usernameUnique);
    },
    usernameFieldFeedback() {
      if (!this.$v.username.required) return 'Username is required';
      return !this.$v.username.usernameUnique ? 'Username already taken'
        : 'Must be at least 3 characters';
    },
    emailFieldError() {
      return this.signUpStatus.submitClicked
        && (!this.$v.email.email || !this.$v.email.required || !this.$v.email.emailUnique);
    },
    emailFieldFeedback() {
      if (!this.$v.email.required) return 'Email is required';
      return !this.$v.email.emailUnique ? 'Email already in use' : 'Email invalid';
    },
    passwordFieldError() {
      return this.signUpStatus.submitClicked && (!this.$v.password.required
        || !this.$v.password.minLength || !this.$v.confirmPass.sameAsPassword);
    },
    passwordFieldFeedback() {
      if (!this.$v.password.required) return 'Password required';
      return !this.$v.password.minLength ? 'Password must be at least 7 characters' : '';
    },
    passwordMatchFeedback() {
      return !this.$v.confirmPass.sameAsPassword && (this.$v.password.required
        && this.$v.password.minLength) ? 'Passwords must match' : '';
    }
  }
};
</script>
<style>
  #signup_card input {
    border-radius: 5px;
    background-color: #323645;
    border-color: #323645;
    color: #FFFFFF;
    margin-bottom: 12px;
    font-family: 'Open Sans', sans-serif;
  }
  #signup_card .err_txt_layout {
    margin-top: -11px;
  }
</style>

<style scoped>
  #signup_card {
    width: auto;
    background-color: #272a36;
    border-radius: 5px;
    padding: 10px 15px 10px 15px;
  }

  #signup_btn {
    background-color: #DB564E;
    border-color: #DB564E;
    margin-top: 10px;
    width: 165px;
    font-family: 'Open Sans', sans-serif;
  }
</style>
