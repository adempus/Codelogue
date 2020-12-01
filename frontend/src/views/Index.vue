<template>
  <div class="p-d-flex p-jc-center">
    <div class="p-d-flex p-flex-column" style="width: 20vw;">
      <div class="p-mb-2">
        <TabMenu :model="items" id="credentialsMenu" />
      </div>
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "Index",
  components: {},
  data() {
    return {
      items: [
        {
          label: "Sign In",
          to: "/sign-in",
          // command usages necessary to prevent breaking of form validation state when tabs are toggled.
          command: () => {
            location.replace("/sign-in");
          }
        },
        {
          label: "Sign Up",
          to: "/sign-up",
          command: () => {
            location.replace("sign-up");
          }
        }
      ]
    };
  }
};
</script>

<style>
.p-tabmenu .p-tabmenu-nav {
  background: #272a36 !important;
  border: none !important;
  margin-bottom: -9px;
}
.p-tabmenu .p-tabmenu-nav .p-tabmenuitem.p-highlight .p-menuitem-link {
  background: #272a36 !important;
  border-color: #db564e !important;
  color: #db564e !important;
}
.p-tabmenu .p-tabmenu-nav .p-tabmenuitem .p-menuitem-link {
  border-width: 0 0 1px 0 !important;
  border-color: #272a36 !important;
  background: #272a36 !important;
  color: #6c757d;
  border-top-right-radius: 5px !important;
  border-top-left-radius: 5px !important;
  margin: 0 0 0 0 !important;
}
.p-menuitem-link:focus {
  outline: none !important;
  box-shadow: none !important;
}
a.p-menuitem-link {
  width: 10vw !important;
}
</style>
