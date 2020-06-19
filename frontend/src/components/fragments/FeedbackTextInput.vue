<template>
    <div :class="fieldPayload.layout">
        <!-- input -->
        <InputText v-model="inputValue"
                   :type="fieldPayload.inputType"
                   :placeholder="fieldPayload.placeholder"
                   :class="[{ 'p-invalid': fieldPayload.isFieldError }, fieldPayload.size]"/>
        <!-- error message -->
        <div class="err_txt_layout">
            <small class="error_txt" v-if="fieldPayload.isFieldError">
                {{ fieldPayload.fieldFeedback }}
            </small>
        </div>
    </div>
</template>

<script>
export default {
  name: 'FeedbackTextInput',
  data() {
    return {
      inputValue: this.value
    };
  },
  props: ['fieldPayload', 'value'],
  watch: {
    inputValue() {
      this.$emit('input', this.inputValue);
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
