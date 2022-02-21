import Vue from 'vue'
import VueRouter from 'vue-router'
import AuthLogin from '@/components/AuthLogin';
import MainPage from '@/components/MainPage';
import store from '@/store'

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    console.log("11111111")
    next()
    return
  }
  console.log("22222222222")
  next('')
}
const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    console.log("333333333333")
    next()
    return
  }
  console.log("44444444444")
  next('/login')
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