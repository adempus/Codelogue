import { createApp, provide, h } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import { VuelidatePlugin } from "@vuelidate/core";
import { ApolloClient, InMemoryCache } from "@apollo/client";
import { DefaultApolloClient } from "@vue/apollo-composable";
import { HttpLink } from "@apollo/client";
import { setContext } from "@apollo/client/link/context";

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

const httpLink = new HttpLink({
  uri: "http://127.0.0.1:5001/graphql"
});

const authMiddleware = setContext(() => ({
  headers: {
    authorization: store.getters.getAccessToken
  }
}));

const link = authMiddleware.concat(httpLink);

const apolloClient = new ApolloClient({
  link,
  cache: new InMemoryCache()
});

const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient);
  },
  render() {
    return h(App);
  }
});

app.use(store);
app.use(router);
app.use(VuelidatePlugin);
app.use(ToastService);
app.component("Button", Button);
app.component("Dialog", Dialog);
app.component("Menubar", Menubar);
app.component("InputText", InputText);
app.component("TabMenu", TabMenu);
app.component("Card", Card);
app.component("Toast", Toast);
app.mount("#app");

export default app;
