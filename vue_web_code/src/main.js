import Vue from 'vue'
import App from './App.vue'
import jsPDF from 'jspdf'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import router from './router'
import store from './store'

require('./assets/css/main.css')

Vue.config.productionTip = false

Vue.use(Buefy)
Vue.use(VueAxios, axios)
Vue.use(jsPDF)

new Vue({
  router,
  store,
  beforeCreate () {
    this.$http.defaults.baseURL = '/api/v1'
    this.$store.commit('initialiseStore')
    this.$http.defaults.headers.common['Authorization'] = this.$store.state.access
    if (this.$store.state.isLoggedIn === false) {
      if (this.$router.currentRoute.path !== '/login') {
        this.$router.push('/login')
      }
    } else {
      if (this.$router.currentRoute.path === '/login') {
        this.$router.push('/')
      } else {
        this.$router.push(this.$router.currentRoute.path)
      }
    }
  },
  created () {
    this.$http.interceptors.response.use(
      response => response,
      (error) => {
        if (error.response.status === 401) {
          this.$store.commit('logout')
          this.$router.push('/login')
        }
        return Promise.reject(error.response)
      })
    this.$router.beforeEach(async (to, from, next) => {
      // Refresh access token
      this.$http.post('refresh-token/', {refresh: this.$store.state.refresh}).then(response => {
        if (response.data.error) {
          this.$store.commit('logout')
          next({ name: 'login' })
        } else {
          this.$http.defaults.headers.common['Authorization'] = response.data.access
          this.$store.commit('refresh', {
            access: response.data.access
          })
        }

        // Do the actual page request
        if (to.name !== 'login' && !this.$store.state.isLoggedIn) {
          next({ name: 'login' })
        } else {
          if (to.name === 'login' && this.$store.state.isLoggedIn) {
            next({name: '/'})
          } else {
            next()
          }
        }
      })
    })
  },
  render: h => h(App)
}).$mount('#app')
