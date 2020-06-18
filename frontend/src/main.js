// PrimeVue components
import Button from 'primevue/button';
import Menubar from 'primevue/menubar';
import InputText from 'primevue/inputtext';
import Card from 'primevue/card';
import ToastService from 'primevue/toastservice';
import Toast from 'primevue/toast';


// vuelidate for form validation
import Vuelidate from 'vuelidate';

import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

// Custom components
import Navbar from './components/Navbar.vue';
import Landing from './components/Landing.vue';
import SignInForm from './components/SignInForm.vue';
import SignUpForm from './components/SignUpForm.vue';
import SignInEmailInput from './components/fragments/SignInEmailInput.vue';
import SignInPasswordInput from './components/fragments/SignInPasswordInput.vue';

// server endpoint urls
import endpoints from './router/endpoints';

import 'primevue/resources/themes/saga-blue/theme.css'; // theme
import 'primevue/resources/primevue.min.css'; // core css
// Importing the base PrimeIcon styles
import 'primeicons/primeicons.css';
// import PrimeFlex for positioning
import 'primeflex/primeflex.css';

// Register global components
Vue.component('Button', Button);
Vue.component('Menubar', Menubar);
Vue.component('InputText', InputText);
Vue.component('Card', Card);
Vue.component('Navbar', Navbar);
Vue.component('Landing', Landing);
Vue.component('SignInForm', SignInForm);
Vue.component('SignUpForm', SignUpForm);
Vue.component('SignInEmailInput', SignInEmailInput);
Vue.component('SignInPasswordInput', SignInPasswordInput);
Vue.component('Toast', Toast);

Vue.use(Vuelidate);
Vue.use(ToastService);
Vue.config.productionTip = false;


new Vue({
  router,
  data: endpoints,
  store,
  render: (h) => h(App),
}).$mount('#app');
