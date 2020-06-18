<template>
    <div class="p-field p-fluid">
        <!-- password input -->
        <InputText v-model="value"
                   type="password" placeholder="Password"
                   class="p-inputtext-sm login_txtbox"
                   aria-describedby="password_feedback"
                   :class="{ 'p-invalid': loginPasswordFieldError }"/>
        <!-- password error message -->
        <div class="password_error_div">
            <small class="error_txt" id="password_feedback" v-if="loginPasswordFieldError">
                {{ loginPasswordFeedback }}
            </small>
        </div>
    </div>
</template>

<script>
export default {
  name: 'SignInPasswordInput',
  props: ['value', 'loginPasswordFieldError', 'loginPasswordFeedback'],
  watch: {
    value() {
      this.$emit('input', this.value);
    }
  }
};
</script>

<style scoped>

</style>
