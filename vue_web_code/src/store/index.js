import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    isLoggedIn: false,
    refresh: null,
    access: null,
    username: null,
    isAdmin: false
  },
  mutations: {
    initialiseStore (state) {
      if (localStorage.getItem('access')) {
        state.isLoggedIn = true
        state.access = localStorage.getItem('access')
        state.refresh = localStorage.getItem('refresh')
        state.username = localStorage.getItem('username')
        state.isAdmin = localStorage.getItem('is_admin')
      }
    },
    login (state, payload) {
      state.isLoggedIn = true
      state.access = payload.access
      state.refresh = payload.refresh
      state.username = payload.username
      state.isAdmin = payload.isAdmin
      localStorage.setItem('access', state.access)
      localStorage.setItem('refresh', state.refresh)
      localStorage.setItem('username', state.username)
      localStorage.setItem('is_admin', state.isAdmin)
      console.log('payload:', payload)
    },
    refresh (state, payload) {
      state.access = payload.access
    },
    logout (state) {
      state.isLoggedIn = false
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      localStorage.removeItem('username')
      localStorage.removeItem('is_admin')
    }
  }
})

export default store
