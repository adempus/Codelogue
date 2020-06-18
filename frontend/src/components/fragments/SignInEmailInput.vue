<template>
    <div class="p-field p-fluid">
        <!-- email input -->
        <InputText v-model="value"
                   type="email" placeholder="Email"
                   class="p-inputtext-sm login_txtbox"
                   aria-describedby="email_feedback"
                   :class="{ 'p-invalid': loginEmailFieldError }"/>
        <!-- email error message -->
        <div class="email_error_div">
            <small class="error_txt" id="email_feedback" v-if="loginEmailFieldError">
                {{ loginEmailFeedback }}
            </small>
        </div>
    </div>
</template>

<script>
export default {
  name: 'SignInEmailInput',
  props: ['value', 'loginEmailFieldError', 'loginEmailFeedback'],
  watch: {
    value() {
      this.$emit('input', this.value);
    }
  }
};
</script>

<style scoped>

</style>
