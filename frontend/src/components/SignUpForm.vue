<template>
  <Card id="signup_card">
    <template slot="content">
      <div class="p-fluid p-formgrid p-grid p-justify-center">
        <!-- first name input -->
        <FeedbackTextInput
            :value="firstName"
            :field-payload="getInputFieldPayload(
              'p-field p-col-6', firstNameFieldError, 'First name is required', 'First Name')"
            :state="validateState('firstName')"
            @input="(fNameInput) => { this.firstName = fNameInput }"/>

        <!-- last name input -->
        <FeedbackTextInput
            :value="lastName"
            :field-payload="getInputFieldPayload(
              'p-field p-col-6', lastNameFieldError, 'Last name is required', 'Last Name')"
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
        <Button @click="signUpUser()"
                type="button" label="Sign Up" class="p-button-sm " id="signup_btn"/>
      </div>
    </template>
  </Card>
</template>

<script>
import { required, minLength, sameAs, email } from 'vuelidate/lib/validators';

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
        submitted: false
      },
      response: {},
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
      // usernameUnique,
    },
    email: {
      required,
      email,
      // emailUnique,
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
    signUpUser() {
      this.$set(this.signUpStatus, 'submitted', true);
      this.$v.$touch();
    },
  },
  computed: {
    firstNameFieldError() {
      return this.signUpStatus.submitted && !this.$v.firstName.required;
    },
    lastNameFieldError() {
      return this.signUpStatus.submitted && !this.$v.lastName.required;
    },
    usernameFieldError() {
      return this.signUpStatus.submitted
        && (!this.$v.username.required || !this.$v.username.minLength);
    },
    usernameFieldFeedback() {
      return !this.$v.username.minLength ? 'Username must be at least 3 characters'
        : 'Username is required';
    },
    emailFieldError() {
      return this.signUpStatus.submitted && (!this.$v.email.email || !this.$v.email.required);
    },
    emailFieldFeedback() {
      return !this.$v.email.email ? 'Email is invalid' : 'Email is required';
    },
    passwordFieldError() {
      return this.signUpStatus.submitted && (!this.$v.password.required
        || !this.$v.password.minLength || !this.$v.confirmPass.sameAsPassword);
    },
    passwordFieldFeedback() {
      if (!this.$v.password.required) {
        return 'Password is required';
      }
      if (!this.$v.password.minLength) {
        return 'Password must be at least 7 characters';
      }
      return '';
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
