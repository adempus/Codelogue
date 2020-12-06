<template style="padding-bottom: 50px;">
  <Card id="card_input">
    <template v-slot:content>
      <form v-on:keyup.enter="submit" class="p-fluid">
        <!-- email input -->
        <div class="p-float-label p-field" style="margin-bottom: 20px;">
          <InputText id="email" type="text" v-model="signInForm.email" />
          <label for="email" class="signin_label">Email</label>
        </div>
        <!-- password input -->
        <div class="p-float-label p-field">
          <InputText
            id="password"
            type="password"
            v-model="signInForm.password"
          />
          <label for="password" class="signin_label">Password</label>
        </div>
        <!-- sign-in button -->
        <div class="p-col" style="padding-top: 20px;">
          <Button
            type="button"
            @click="submit"
            icon="pi pi-chevron-right"
            class="p-button-rounded p-button-outlined login_btn"
          />
        </div>
      </form>
    </template>
    <!-- credential feedback -->
    <template #footer>
      <div v-if="signInFormError">
        <div v-for="(error, index) of allErrorFeedback" :key="index">
          <small class="p-invalid">{{ error }}</small>
        </div>
      </div>
      <div v-else-if="signInSuccess">
        <small class="p-valid">Sign in successful</small>
      </div>
    </template>
  </Card>
</template>

<script>
import { required, email } from "@vuelidate/validators";
import { useMutation } from "@vue/apollo-composable";
import signInMutation from "../graphql/mutations/signIn.mutation.graphql";

export default {
  name: "SignIn",
  setup() {
    const { mutate: signInUser } = useMutation(signInMutation);
    return { signInUser };
  },
  data() {
    return {
      signInForm: {
        email: "",
        password: "",
        response: null
      },
      inputAttempt: {
        email: "",
        password: ""
      }
    };
  },
  validations() {
    return {
      signInForm: {
        email: {
          email,
          required
        },
        password: {
          required
        }
      }
    };
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (this.$v.$error) return; // form error check
      this.trackInputAttempt();
      this.signInUser({
        email: this.signInForm.email,
        password: this.signInForm.password
      })
        .then(res => (this.signInForm.response = res["data"]["signInUser"]))
        .catch(err => console.log("An error has occurred: ", err))
        .finally(() => {
          if (this.signInSuccess) {
            this.storeTokens();
            this.$router.push("dashboard");
          }
        });
    },
    trackInputAttempt() {
      this.inputAttempt.email = this.signInForm.email;
      this.inputAttempt.password = this.signInForm.password;
    },
    storeTokens() {
      localStorage.clear(); // flush old if any
      localStorage.setItem(
        "accessToken",
        `Bearer ${this.signInForm.response["accessToken"]}`
      );
      localStorage.setItem(
        "refreshToken",
        this.signInForm.response["refreshToken"]
      );
    }
  },
  computed: {
    signInFormError() {
      return (
        this.$v.signInForm.$errors.length > 0 ||
        (this.signInResponseError && this.newInputBad)
      );
    },
    signInResponseError() {
      return (
        this.signInForm.response !== null &&
        this.signInForm.response.error === true
      );
    },
    signInResponseErrorFeedback() {
      if (!this.signInResponseError) return "";
      return this.signInForm.response.message;
    },
    newInputBad() {
      if (!this.signInResponseError) return false;
      if (this.signInForm.response["passwordInvalid"])
        return (
          this.inputAttempt.password.toLowerCase() ===
          this.signInForm.password.toLowerCase()
        );
      else if (this.signInForm.response["userNotFound"])
        return (
          this.inputAttempt.email.toLowerCase() ===
          this.signInForm.email.toLowerCase()
        );
      return false;
    },
    emailError() {
      return this.$v.signInForm.email.$error;
    },
    emailErrorFeedback() {
      if (!this.emailError) return "";
      return this.$v.signInForm.email.required.$invalid
        ? "Email is required"
        : this.$v.signInForm.email.email.$message;
    },
    passwordError() {
      return this.$v.signInForm.password.$error;
    },
    passwordErrorFeedback() {
      if (!this.passwordError) return "";
      return this.$v.signInForm.password.required.$invalid
        ? "Password is required"
        : this.$v.signInForm.password.required.$message;
    },
    signInSuccess() {
      if (this.signInForm.response === null) return false;
      return (
        this.signInForm.response["__typename"] === "UserSignInSuccessOutput"
      );
    },
    allErrorFeedback() {
      return [
        this.emailErrorFeedback,
        this.passwordErrorFeedback,
        this.signInResponseErrorFeedback
      ];
    }
  }
};
</script>

<style>
#card_input {
  width: 20vw;
  background-color: #272a36;
  border-radius: 5px;
  padding: 15px 15px 0 15px;
}
#card_input input {
  border-radius: 5px;
  background-color: #323645;
  border-color: #323645;
  color: #ffffff;
  font-family: "Open Sans", sans-serif;
  margin-top: 15px;
}
#signin_btn {
  background-color: #db564e;
  border-color: #db564e;
  width: 100px;
  margin-top: 25px;
  font-family: "Open Sans", sans-serif;
}
#signin_header {
  color: #db564e;
  font-family: "NTR", sans-serif;
  margin: 0 0 -15px 0;
  text-align: left;
  font-weight: 500;
}
.signin_label {
  padding-top: 10px;
}
.error_txt {
  color: #eb897e;
  font-size: 0.75rem;
  font-family: "Open Sans", sans-serif;
}
.p-invalid {
  border-color: #eb897e !important;
}
.p-valid {
  color: #00cd6f;
}
.success_msg {
  color: #00cd6f;
  font-size: 13px;
  padding-top: 5px;
  text-align: right;
}
.login_btn {
  border-color: #db564e;
  color: #db564e !important;
  outline-color: #db564e;
}
</style>

<style scoped>
.separator {
  margin-bottom: 30px;
}
</style>
