import Vue from 'vue'
import VueRouter from 'vue-router'
import Password from '@/components/Password'
import Home from '@/components/Home'
import Login from '@/components/Login'
import LandingPage from '@/components/LandingPage'

Vue.use(VueRouter)

const routes = [
  { path: '/login', component: Login, name: 'login' },
  { path: '/', component: Home },
  { path: '/password', component: Password },
  { path: '/LandingPage', component: LandingPage }
]

const router = new VueRouter({
  routes
})

export default router
