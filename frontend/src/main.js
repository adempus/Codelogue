import { createApp, provide, h } from "vue";
import App from "@/App.vue";
import router from "@/router";
import store from "@/store";
import mitt from "mitt";
import { VuelidatePlugin } from "@vuelidate/core";
import { DefaultApolloClient } from "@vue/apollo-composable";
import apolloClient from "@/graphql";
// PrimeVue imports
import "primeflex/primeflex.css";
import "primevue/resources/themes/saga-blue/theme.css"; // theme
import "primevue/resources/primevue.min.css"; // core css
import "primeicons/primeicons.css"; // icons
// components
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import Menubar from "primevue/menubar";
import InputText from "primevue/inputtext";
import Card from "primevue/card";
import TabMenu from "primevue/tabmenu";
import ToastService from "primevue/toastservice";
import Toast from "primevue/toast";
import Tree from "primevue/tree";
import ScrollPanel from "primevue/scrollpanel";
import ToggleButton from "primevue/togglebutton";
import BlockUI from "primevue/blockui";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Tag from "primevue/tag";
import Chips from "primevue/chips";
import Ripple from "primevue/ripple";
import Dropdown from "primevue/dropdown";
import Editor from "primevue/editor";
import Textarea from "primevue/textarea";

// import Inplace from "primevue/inplace";

const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient);
  },
  render() {
    return h(App);
  }
});

const emitter = mitt();
app.config.globalProperties.emitter = emitter;

app.use(store);
app.use(router);
app.use(VuelidatePlugin);
app.use(ToastService);
app.directive("ripple", Ripple);
app.component("Button", Button);
app.component("Dialog", Dialog);
app.component("Menubar", Menubar);
app.component("InputText", InputText);
app.component("TabMenu", TabMenu);
app.component("Card", Card);
app.component("Toast", Toast);
app.component("Tree", Tree);
app.component("DataTable", DataTable);
app.component("Column", Column);
app.component("ScrollPanel", ScrollPanel);
app.component("ToggleButton", ToggleButton);
app.component("BlockUI", BlockUI);
app.component("Tag", Tag);
app.component("Chips", Chips);
// app.component("Inplace", Inplace);
app.component("Dropdown", Dropdown);
app.component("Editor", Editor);
app.component("Textarea", Textarea);
app.mount("#app");

export default app;
