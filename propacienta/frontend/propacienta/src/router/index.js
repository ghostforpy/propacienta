import Vue from 'vue'
import VueRouter from 'vue-router'
import AuthLogin from '@/views/auth/AuthLogin';
import AuthLogout from '@/views/auth/AuthLogout';
import MainPage from '@/components/MainPage';
// import store from '@/store'
// import { AUTH_PING } from "@/store/actions/auth";
import { ifAuthenticated, ifNotAuthenticated } from './utils';
// import RegistrationRouter from './registration'
import RegistrationView from '@/views/registration/Registration';



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
    component: AuthLogout,
    beforeEnter: ifAuthenticated,
    meta: { requiresAuth: true }
  },
  {
    path: '/registration',
    name: 'registration',
    component: RegistrationView,
    beforeEnter: ifNotAuthenticated,
  },
  {
    path: '',
    name: "main",
    component: MainPage,
    //beforeEnter: ifAuthenticated,
    //meta: { requiresAuth: true }
  },

]
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router