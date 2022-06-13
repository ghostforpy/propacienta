import Vue from 'vue';
import Vuex from 'vuex';
import auth from "./modules/auth";
import chats from "./modules/chats";
import pacient from "./modules/pacient";
import registraion from "./modules/registration";
import user from "./modules/user";

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    user,
    auth,
    registraion,
    pacient,
    chats
  },
})
