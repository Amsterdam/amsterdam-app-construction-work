import Vue from 'vue'
import VueRouter from 'vue-router'
import Password from '@/components/Password'
import Login from '@/components/Login'
import AccountBeheer from '@/components/AccountBeheer'
import BerichtenBeheer from '@/components/BerichtenBeheer'

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch((err) => err)
}

Vue.use(VueRouter)

const routes = [
  { path: '/login', component: Login, name: 'login' },
  { path: '/password', component: Password },
  { path: '/', component: AccountBeheer },
  { path: '/berichtenbeheer', component: BerichtenBeheer },
]

const router = new VueRouter({
  routes,
})

export default router
