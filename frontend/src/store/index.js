import { createStore } from "vuex";
import apolloClient from "@/graphql";
// import {gql} from "@apollo/client";
import checkAuthorizationMutation from "../graphql/mutations/checkAuthorization.mutation.graphql";

export default createStore({
  state() {
    return {
      count: 0,
      accessToken: null,
      authResponse: null,
      userInfo: null,
      signedIn: false
    };
  },
  getters: {
    getCount: state => {
      return state.count;
    },
    getAccessToken: state => {
      return state.accessToken;
    },
    getUserInfo: state => {
      return state.userInfo;
    },
    authorizationState: state => {
      return state.authResponse;
    },
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
    },
    storeAuthorizationState: (state, payload) => {
      state.authResponse = payload;
    },
    storeUserInfo: (state, payload) => {
      state.userInfo = payload;
    }
  },
  actions: {
    increment: context => {
      context.commit("increment");
    },
    decrement: context => {
      context.commit("decrement");
    },
    checkUserAuthorization: context => {
      apolloClient
        .mutate({ mutation: { ...checkAuthorizationMutation } })
        .then(res =>
          context.commit(
            "storeAuthorizationState",
            res["data"]["checkAuthorization"]
          )
        )
        .catch(err => console.log("An error occurred", err))
        .finally(() => {
          if (!context.getters.authorizationState.error)
            context.commit(
              "storeUserInfo",
              context.getters.authorizationState["user"]
            );
          console.log(context.getters.authorizationState);
        });
    },
    storeAccessToken: context => {
      context.commit("storeAccessToken");
    }
  },
  modules: {}
});
