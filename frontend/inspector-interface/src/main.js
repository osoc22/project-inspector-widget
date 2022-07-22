import Vue from 'vue'
import App from './App.vue'
import Buefy from 'buefy'
import VueRouter from 'vue-router'
import 'buefy/dist/buefy.css'
import ScraperDashboard from './views/ScraperDashboard'
import LandingPage from './views/LandingPage'
import {createStore} from 'vuex'
import mdiVue from 'mdi-vue/v2'
import * as mdijs from '@mdi/js'


Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    {
      path: '/dashboard',
      component: ScraperDashboard
    },
    {
      path: '/',
      component: LandingPage
    }
  ]
})

const store = createStore({
  state()  {
    return {
      start_date: null,
      end_date: null,
      url: null,
      data: [],
      name: null,
      overview: false

    }
  },
  getters: {
    getStartDate(state) {
      return state.start_date
    },
    getEndDate(state) {
      return state.end_date
    },
    getURL(state){
      return state.url
    },
    getData(state) {
      return state.data
    },
    getName(state) {
      return state.name
    },
    getOverview(state) {
      return state.overview
    }
  },
  mutations: {
    SET_START_DATE(state, input) {
      console.log(input)
      state.start_date = input
    },
    SET_END_DATE(state, input) {
      state.end_date = input
    },
    SET_URL(state, input) {
      state.url = input.target.value
    },
    SET_DATA(state, input) {
      state.data = input
    },
    SET_NAME(state, input) {
      state.name = input.target.value
    },
    SET_OVERVIEW(state, input) {
      state.overview = input
    }
  }
})

Vue.prototype.$store = store
Vue.config.productionTip = false
Vue.use(Buefy)
Vue.use(mdiVue, {
  icons: mdijs
})

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
