<template>
    <div :class="layout">
        <!-- input -->
        <InputText v-model="value"
                   :type="inputType"
                   :placeholder="placeholder"
                   :class="[{ 'p-invalid': isFieldError }, size]"/>
        <!-- error message -->
        <div class="err_txt_layout">
            <small class="error_txt" v-if="isFieldError"> {{ fieldFeedback }} </small>
        </div>
    </div>
</template>

<script>
export default {
  name: 'FeedbackTextInput',
  props: ['layout', 'value', 'isFieldError', 'fieldFeedback', 'inputType', 'placeholder', 'size'],
  watch: {
    value() {
      this.$emit('input', this.value);
    }
  }
};
</script>

<style scoped>
    .err_txt_layout {
        position: absolute;
        text-align: left;
        padding-left: 5px;
    }
</style>
