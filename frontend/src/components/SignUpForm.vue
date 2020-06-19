<template>
    <Card id="signup_card">
        <template slot="content">
            <div class="p-fluid p-formgrid p-grid p-justify-center">
              <!-- first name input -->
              <FeedbackTextInput
                      :value="firstName"
                      :layout="'p-field p-col-6'"
                      :is-field-error="firstNameFieldError"
                      :field-feedback="'First name is required'"
                      :placeholder="'First Name'"
                      :state="validateState('firstName')"
                      @input="(fNameInput) => { this.firstName = fNameInput }">
              </FeedbackTextInput>

              <!-- last name input -->
              <FeedbackTextInput
                      :value="lastName"
                      :layout="'p-field p-col-6'"
                      :is-field-error="lastNameFieldError"
                      :field-feedback="'Last name is required'"
                      :placeholder="'Last Name'"
                      :state="validateState('lastName')"
                      @input="(lNameInput) => { this.lastName = lNameInput }">
              </FeedbackTextInput>

              <!-- username input -->
              <FeedbackTextInput
                      :value="username"
                      :layout="'p-field p-col-12'"
                      :is-field-error="usernameFieldError"
                      :field-feedback="usernameFieldFeedback"
                      :placeholder="'Username'"
                      :state="validateState('username')"
                      @input="(usernameInput) => { this.username = usernameInput }">
              </FeedbackTextInput>

              <!-- email input -->
              <FeedbackTextInput
                      :value="email"
                      :layout="'p-field p-col-12'"
                      :is-field-error="emailFieldError"
                      :field-feedback="emailFieldFeedback"
                      :placeholder="'Email address'"
                      :input-type="'email'"
                      :state="validateState('email')"
                      @input="(emailInput) => { this.email = emailInput }">
              </FeedbackTextInput>

              <!-- password input -->
              <FeedbackTextInput
                      :value="password"
                      :layout="'p-field p-col-6'"
                      :is-field-error="passwordFieldError"
                      :field-feedback="passwordFieldFeedback"
                      :placeholder="'Password'"
                      :input-type="'password'"
                      :state="validateState('password')"
                      @input="(passwordInput) => { this.password = passwordInput }">
              </FeedbackTextInput>

              <!-- password confirmation -->
              <FeedbackTextInput
                      :value="confirmPass"
                      :layout="'p-field p-col-6'"
                      :is-field-error="passwordFieldError"
                      :field-feedback="passwordMatchFeedback"
                      :placeholder="'Confirm Password'"
                      :input-type="'password'"
                      :state="validateState('confirmPass')"
                      @input="(confirmPassInput) => { this.confirmPass = confirmPassInput }">
              </FeedbackTextInput>

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
