import Vue from 'vue'
import Vuex from 'vuex'
//import user from "./modules/user";
import auth from "./modules/auth";
import registraion from "./modules/registration"

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
    //   user,
    auth,
    registraion
  },
})
