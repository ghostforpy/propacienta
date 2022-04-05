import MainPage from '@/components/MainPage';
import NotFound from '@/components/NotFound';
import AuthLogin from '@/views/auth/AuthLogin';
import AuthLogout from '@/views/auth/AuthLogout';
import Vue from 'vue';
import VueRouter from 'vue-router';
import MedicineCard from './medicinecard';
import RegistrationRoutes from './registration';
import UsersRoutes from './users';
// import store from '@/store'
// import { AUTH_PING } from "@/store/actions/auth";
import { ifAuthenticated, ifNotAuthenticated } from './utils';


Vue.use(VueRouter)
const baseRoutes = [
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
    path: '',
    name: "main",
    component: MainPage,
    //beforeEnter: ifAuthenticated,
    //meta: { requiresAuth: true }
  },
  {
    path: '*',
    name: "notfound",
    component: NotFound,
    // beforeEnter: ifNotAuthenticated,
  },
]
var routes = baseRoutes.concat(UsersRoutes);
routes = routes.concat(RegistrationRoutes)
routes = routes.concat(MedicineCard)
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router