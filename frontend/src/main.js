// PrimeVue components
import Button from 'primevue/button';
import Menubar from 'primevue/menubar';
import InputText from 'primevue/inputtext';
import Card from 'primevue/card';
import ToastService from 'primevue/toastservice';
import Toast from 'primevue/toast';
import Dialog from 'primevue/dialog';

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
import FeedbackTextInput from './components/subcomponents/FeedbackTextInput.vue';

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
Vue.component('FeedbackTextInput', FeedbackTextInput);
Vue.component('Toast', Toast);
Vue.component('Dialog', Dialog);

Vue.use(Vuelidate);
Vue.use(ToastService);
Vue.config.productionTip = false;

Vue.mixin({
  methods: {
    getInputFieldPayload(layout, isFieldError, fieldFeedback,
      placeholder, size = '', inputType = 'text') {
      return {
        layout: layout,
        isFieldError: isFieldError,
        fieldFeedback: fieldFeedback,
        inputType: inputType,
        placeholder: placeholder,
        size: size
      };
    },
    /**
     * To clear field error messages on signup and signin forms, after corrections are made to them,
     * post server side validation.
     * */
    applyFieldChange(formStatusObj, statusErrorObj, errObjName, condition) {
      if (formStatusObj.response !== null) {
        if (formStatusObj.submitClicked && formStatusObj.response.error) {
          if (statusErrorObj) this.$set(formStatusObj, errObjName, condition);
        }
      }
    }
  }
});

new Vue({
  router,
  data: endpoints,
  store,
  render: (h) => h(App),
}).$mount('#app');
