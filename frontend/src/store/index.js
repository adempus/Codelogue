import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import endpoints from '../router/endpoints';

Vue.use(Vuex);

const store = new Vuex.Store({
  // reactive equivalent to vue instance data attributes
  state: {
    isSignedIn: false,
    username: null,

  },
  mutations: {
    // used to commit and track changes to state.
    // enables time traveling to rollback state changes.
    setSignInState(currentState, newState) {
      currentState.isSignedIn = newState;
    },
    setUsername(currentState, newState) {
      currentState.username = newState;
    }
  },
  actions: {
    // used to call mutations to update state directly
    setStateSignedIn(context) {
      context.commit('setSignInState', true);
    },
    updateSignInValidation(context) {
      if (localStorage.getItem('token') !== null) {
        axios.get(endpoints.auth, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }).then((response) => {
          console.log('auth response: ', response);
          const res = response.data;
          if (res.error) {
            console.log('sign in error: ', res.msg);
            context.commit('setSignInState', false);
            context.commit('setUsername', null);
          } else {
            context.commit('setSignInState', true);
            context.commit('setUsername', res.user.username);
          }
        });
      }
    },
    setStateSignedOut(context) {
      context.commit('setSignInState', false);
      context.commit('setUsername', null);
    },
  },
  getters: {
    // accesses state
    isSignedIn(state) {
      return state.isSignedIn;
    },
    username(state) {
      return state.username;
    }
  },
});

export default store;
