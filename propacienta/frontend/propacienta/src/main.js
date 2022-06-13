import VTooltip from 'v-tooltip'
import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import store from './store'

Vue.config.productionTip = false
Vue.use(VTooltip)

new Vue({
  router,
  vuetify,
  store,
  render: h => h(App)
}).$mount('#app')
