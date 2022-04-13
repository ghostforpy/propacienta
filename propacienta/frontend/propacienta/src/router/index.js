import AuthLogin from '@/views/auth/AuthLogin';
import AuthLogout from '@/views/auth/AuthLogout';
import PasswordForgot from '@/views/auth/PasswordForgot';
import PasswordForgotConfirm from '@/views/auth/PasswordForgotConfirm';
import MainPage from '@/views/MainPage';
import NotFound from '@/views/NotFound';
import Vue from 'vue';
import VueRouter from 'vue-router';
import DoctorsRoutes from './doctors';
import MedicineCard from './medicinecard';
import PacientsRoutes from './pacients';
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
    path: '/recover-password',
    name: "recover-password",
    component: PasswordForgot,
    beforeEnter: ifNotAuthenticated,
  },
  {
    path: '/password-reset-confirm/:uid/:token',
    name: "password-reset-confirm",
    component: PasswordForgotConfirm,
    beforeEnter: ifNotAuthenticated,
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
routes = routes.concat(DoctorsRoutes)
routes = routes.concat(PacientsRoutes)
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router