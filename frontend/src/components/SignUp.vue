<template>
  <Toast position="top-right" />
  <Card id="card_input">
    <template v-slot:content>
      <form class="p-fluid p-formgrid p-grid">
        <!-- username input -->
        <div class="p-float-label p-field p-col-12" style="margin-bottom: 20px;">
          <InputText id="username" type="text" v-model="signUpForm.username" />
          <label for="username" class="signin_label inputPadding"
            >Username</label
          >
        </div>
        <!-- email input -->
        <div class="p-float-label p-field p-col-12" style="margin-bottom: 20px;">
          <InputText id="email" type="text" v-model="signUpForm.email" />
          <label for="email" class="signin_label inputPadding">Email</label>
        </div>
        <!-- password -->
        <div class="p-float-label p-field p-col-12 p-md-6" style="margin-bottom: 20px;">
          <InputText
            id="password"
            type="password"
            v-model="signUpForm.password"
          />
          <label for="password" class="signin_label inputPadding"
            >Password</label
          >
        </div>
        <!-- confirm password -->
        <div class="p-float-label p-field p-col-12 p-md-6" style="margin-bottom: 20px;">
          <InputText
            id="password_confirm"
            type="password"
            v-model="signUpForm.passwordConfirm"
          />
          <label for="password_confirm" class="signin_label inputPadding"
            >Confirm</label
          >
        </div>
        <!-- sign-up button -->
        <div class="p-col" style="padding-top: 20px;">
          <Button
            type="button"
            @click="submit"
            icon="pi pi-chevron-right"
            class="p-button-rounded p-button-outlined login_btn"
          />
        </div>
      </form>
      <!-- credential feedback -->
      <div v-if="signUpFormError" class="feedback_section">
        <div
          v-for="(error, index) of [
            usernameErrorFeedback,
            emailErrorFeedback,
            passwordErrorFeedback,
            ...signUpErrorResponseFeedback
          ]"
          :key="index"
        >
          <small class="p-invalid">{{ error }}</small>
        </div>
      </div>
      <div v-else-if="signUpSuccess" class="feedback_section">
        <small class="p-valid">Sign Up successful</small>
      </div>
    </template>
  </Card>
</template>

<script>
import { required, email, sameAs, minLength } from "@vuelidate/validators";
import { useMutation } from "@vue/apollo-composable";
import signUpMutation from "../graphql/mutations/signUp.mutation.graphql";
import { useToast } from "primevue/usetoast";

export default {
  name: "SignUp",
  setup() {
    const { mutate: signUpUser } = useMutation(signUpMutation);
    const toast = useToast();
    return { signUpUser, toast };
  },
  data() {
    return {
      signUpForm: {
        email: "",
        username: "",
        password: "",
        passwordConfirm: "",
        response: null
      },
      inputAttempt: {
        email: "",
        username: ""
      }
    };
  },
  validations() {
    return {
      signUpForm: {
        username: {
          required,
          minLength: minLength(3)
        },
        email: {
          email,
          required
        },
        password: {
          required,
          minLength: minLength(6)
        },
        passwordConfirm: {
          required,
          sameAs: sameAs(this.signUpForm.password, "passwordConfirm")
        }
      }
    };
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (this.$v.$error) return;
      this.trackInputAttempt();
      this.signUpUser({
        username: this.signUpForm.username,
        email: this.signUpForm.email,
        password: this.signUpForm.password
      })
        .then(res => (this.signUpForm.response = res["data"]["signUpUser"]))
        .catch(err => console.log("An error has occurred", err))
        .finally(() => {
          if (this.signUpSuccess) {
            this.notifySuccess();
            setTimeout(() => {
              this.$router.push("sign-in");
            }, 3000);
          }
        });
    },
    trackInputAttempt() {
      this.inputAttempt.username = this.signUpForm.username;
      this.inputAttempt.email = this.signUpForm.email;
    },
    notifySuccess() {
      this.toast.add({
        severity: "success",
        summary: "Sign-Up Success",
        detail: "User registration successful.",
        life: 3000
      });
    }
  },
  computed: {
    signUpFormError() {
      return this.$v.signUpForm.$errors.length > 0 || this.signUpResponseError;
    },
    signUpResponseError() {
      return (
        this.signUpForm.response !== null &&
        this.signUpForm.response.error === true
      );
    },
    signUpErrorResponseFeedback() {
      if (!this.signUpResponseError) return "";
      const errors = [];
      if (this.signUpForm.response["emailExists"])
        errors.push("This email already exists");
      if (this.signUpForm.response["usernameExists"])
        errors.push("This username already exists");
      return errors;
    },
    usernameError() {
      return this.$v.signUpForm.username.$error;
    },
    usernameErrorFeedback() {
      if (!this.usernameError) return "";
      return this.$v.signUpForm.username.required.$invalid
        ? "Username is required"
        : this.$v.signUpForm.username.minLength.$message;
    },
    emailError() {
      return this.$v.signUpForm.email.$error;
    },
    emailErrorFeedback() {
      if (!this.emailError) return "";
      return this.$v.signUpForm.email.required.$invalid
        ? "Email is required"
        : this.$v.signUpForm.email.email.$message;
    },
    passwordError() {
      return (
        this.$v.signUpForm.password.$error ||
        this.$v.signUpForm.passwordConfirm.$error
      );
    },
    passwordErrorFeedback() {
      if (!this.passwordError) return "";
      if (this.$v.signUpForm.password.minLength.$invalid)
        return "Password must be at least 6 letters.";
      else if (this.$v.signUpForm.passwordConfirm.sameAs.$invalid)
        return "Passwords must match.";
      else return "Password is required";
    },
    confirmPasswordError() {
      return this.$v.signUpForm.passwordConfirm.$error;
    },
    signUpSuccess() {
      if (this.signUpForm.response === null) return false;
      return (
        this.signUpForm.response["__typename"] === "UserSignUpSuccessOutput"
      );
    }
  }
};
</script>

<style scoped>
.inputPadding {
  padding-left: 7px;
}

</style>
