import Vue from 'vue'
import VueRouter from 'vue-router'
import AuthLogin from '@/views/auth/AuthLogin';
import MainPage from '@/components/MainPage';
import store from '@/store'
import { AUTH_PING } from "@/store/actions/auth";

const ifNotAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated == '') {
    store.dispatch(AUTH_PING).then(() => {
      if (!store.getters.isAuthenticated) {
        next()
        return
      }
      next('')
    })
  }
}

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated == '') {
    store.dispatch(AUTH_PING).then(() => {
      if (store.getters.isAuthenticated) {
        next()
        return
      }
      next('/login')
    })
  }
}

Vue.use(VueRouter)
const routes = [
  {
    path: '/login',
    name: "login",
    component: AuthLogin,
    beforeEnter: ifNotAuthenticated,
  },
  {
    path: '/logout',
    name: "logout",
    component: AuthLogin,
    beforeEnter: ifAuthenticated,
  },
  {
    path: '',
    name: "main",
    component: MainPage,
    beforeEnter: ifAuthenticated,
    //meta: { requiresAuth: true }
  },

]
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})
export default router