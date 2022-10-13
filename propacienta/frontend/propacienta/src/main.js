import { BrowserTracing } from "@sentry/tracing"
import * as Sentry from "@sentry/vue"
import VTooltip from 'v-tooltip'
import Vue from 'vue'
import { VueReCaptcha } from 'vue-recaptcha-v3'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import store from './store'

Vue.config.productionTip = false
Vue.use(VTooltip)
Vue.prototype.$eventBus = new Vue();


if (process.env.NODE_ENV === "production") {
  const RECAPTCHA_SITE_KEY = process.env.VUE_APP_RECAPTCHA_SITE_KEY
  if (RECAPTCHA_SITE_KEY !== undefined) {
    Vue.use(VueReCaptcha, {
      siteKey: RECAPTCHA_SITE_KEY
      , loaderOptions: {
        autoHideBadge: true
      }
    })
    const SENTRY_DSN = process.env.VUE_APP_SENTRY_DSN
    const BASE_URL = process.env.VUE_APP_BASE_URL
    Sentry.init({
      Vue,
      dsn: SENTRY_DSN,
      integrations: [
        new BrowserTracing({
          routingInstrumentation: Sentry.vueRouterInstrumentation(router),
          tracingOrigins: ["localhost", BASE_URL, /^\//],
        }),
      ],
      // Set tracesSampleRate to 1.0 to capture 100%
      // of transactions for performance monitoring.
      // We recommend adjusting this value in production
      tracesSampleRate: 1.0,
    });
  }


  new Vue({
    router,
    vuetify,
    store,
    render: h => h(App)
  }).$mount('#app')
