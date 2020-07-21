<template>
  <transition appear mode="in-out"
              enter-active-class="animated fadeInUp faster"
              leave-active-class="animated fadeOutDown faster"
              :duration="470">
    <slot></slot>
  </transition>
</template>

<script>
  export default {
    name: 'SignInOutTransition'
  };
</script>

<style scoped>

</style>
