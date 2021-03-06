import Vue from 'vue'
import App from './App.vue'
import Buefy from 'buefy'
import VueRouter from 'vue-router'
import 'buefy/dist/buefy.css'
import ScraperDashboard from './views/ScraperDashboard'
import LandingPage from './views/LandingPage'
import SignIn from './components/SignIn'
import SignUp from './components/SignUp'
import { createStore } from 'vuex'
import mdiVue from 'mdi-vue/v2'
import * as mdijs from '@mdi/js'

Vue.use(VueRouter)

const beforeEnter = (to, from, next) => {
    const isLoggedIn = store.state.access_token

    if (isLoggedIn !== null) {
        if (['home', 'signin', 'signup'].includes(to.name)) {
            next({ name: 'dashboard' })
        } else {
            next()
        }
    } else {
        if (['home', 'signin', 'signup'].includes(to.name)) {
            next()
        } else {
            next({ name: 'home' })
        }
    }
}

const router = new VueRouter({
    routes: [
        {
            name: 'dashboard',
            path: '/dashboard',
            component: ScraperDashboard,
            beforeEnter,
        },
        {
            path: '/',
            name: 'home',
            component: LandingPage,
            beforeEnter,
        },
        {
            name: 'signin',
            path: '/signin',
            component: SignIn,
            beforeEnter,
        },
        {
            name: 'signup',
            path: '/signup',
            component: SignUp,
            beforeEnter,
        },
    ],
})

const store = createStore({
    state() {
        return {
            data: [],
            overview: false,
            access_token: null,
            refresh_token: null,
        }
    },
    getters: {
        getData(state) {
            return state.data
        },
        getOverview(state) {
            return state.overview
        },
        getAccessToken(state) {
            return state.access_token
        },
        getRefreshToken(state) {
            return state.refresh_token
        },
    },
    mutations: {
        SET_DATA(state, input) {
            state.data = input
        },
        SET_OVERVIEW(state, input) {
            state.overview = input
        },
        SET_ACCESS_TOKEN(state, input) {
            state.access_token = input
        },
        SET_REFRESH_TOKEN(state, input) {
            state.refresh_token = input
        },
    },
    actions: {
        disconnect(context) {
            context.commit('SET_ACCESS_TOKEN', null)
            context.commit('SET_REFRESH_TOKEN', null)
            router.push({ name: 'home' })
        },
    },
})

Vue.prototype.$store = store
Vue.config.productionTip = false
Vue.use(Buefy)
Vue.use(mdiVue, {
    icons: mdijs,
})

new Vue({
    router,
    store,
    render: (h) => h(App),
}).$mount('#app')
