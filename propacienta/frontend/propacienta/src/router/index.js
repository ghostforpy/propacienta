import Vue from 'vue'
import VueRouter from 'vue-router'
import AuthLogin from '@/views/auth/AuthLogin';
import MainPage from '@/components/MainPage';
import store from '@/store'
import { AUTH_PING } from "@/store/actions/auth";

// const ifNotAuthenticated = (to, from, next) => {
//   console.log('is not auth', store.getters.isAuthenticated)
//   if (store.getters.isAuthenticated === '') {
//     store.dispatch(AUTH_PING).then(() => {
//       if (!store.getters.isAuthenticated) {
//         next('/login')
//         return
//       }
//       next(from)
//       return
//     })
//   }
//   if (!store.getters.isAuthenticated) {
//     next('/login')
//     return
//   }
//   next(from)
// }

const ifAuthenticated = async (to, from, next) => {
  if (store.getters.isAuthenticated === '') {
    const isAuth = await store.dispatch(AUTH_PING)
    if (isAuth) {
      next()
      return
    }
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  if (store.getters.isAuthenticated) {
    next()
    return
  }
  next({ name: 'login', query: { redirect: to.fullPath } })
}

Vue.use(VueRouter)
const routes = [
  {
    path: '/login',
    name: "login",
    component: AuthLogin,
    //beforeEnter: ifNotAuthenticated,
  },
  {
    path: '/logout',
    name: "logout",
    component: AuthLogin,
    beforeEnter: ifAuthenticated,
    meta: { requiresAuth: true }
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
// router.beforeEach(async (to, from, next) => {
//   console.log(9999999999999, to, from)
//   // var isAuth = false
//   // if (store.getters.isAuthenticated == '') {
//   //   console.log(1)
//   //   isAuth = await store.dispatch(AUTH_PING)//  ascasdsac
//   //   console.log('dsdsds')
//   // } else {
//   //   console.log(11)
//   //   if (store.getters.isAuthenticated) {
//   //     isAuth = true
//   //   } else {
//   //     isAuth = false
//   //   }
//   // }
//   // instead of having to check every route record with
//   // to.matched.some(record => record.meta.requiresAuth)
//   //console.log("isAuth", isAuth)
//   if (to.meta.requiresAuth && !store.getters.isAuthenticated) {
//     console.log(76543234565)
//     // this route requires auth, check if logged in
//     // if not, redirect to login page.
//     next({
//       name: 'login',
//       // save the location we were at to come back later
//       query: { redirect: to.fullPath },
//     })
//   } else {
//     next({
//       path: to
//     })
//   }
// })
export default router