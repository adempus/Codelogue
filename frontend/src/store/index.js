import { createStore } from "vuex";

export default createStore({
  state() {
    return {
      count: 0
    };
  },
  getters: {
    getCount: state => {
      return state.count;
    }
  },
  mutations: {
    increment: state => {
      state.count++;
    },
    decrement: state => {
      state.count--;
    }
  },
  actions: {
    increment: context => {
      context.commit("increment");
    },
    decrement: context => {
      context.commit("decrement");
    }
  },
  modules: {}
});
