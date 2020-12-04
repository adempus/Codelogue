import { createStore } from "vuex";

export default createStore({
  state() {
    return {
      count: 0,
      accessToken: null
    };
  },
  getters: {
    getCount: state => {
      return state.count;
    },
    getAccessToken: state => {
      return state.accessToken;
    }
  },
  mutations: {
    increment: state => {
      state.count++;
    },
    decrement: state => {
      state.count--;
    },
    storeAccessToken: state => {
      state.accessToken = localStorage.getItem("accessToken");
    }
  },
  actions: {
    increment: context => {
      context.commit("increment");
    },
    decrement: context => {
      context.commit("decrement");
    },
    storeAccessToken: context => {
      context.commit("storeAccessToken");
    }
  },
  modules: {}
});
