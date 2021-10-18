import Vue from 'vue'
import VueRouter from 'vue-router'
import Password from '@/components/Password'
import Login from '@/components/Login'
import AccountBeheer from '@/components/AccountBeheer'
import OtherPage from '@/components/OtherPage'

Vue.use(VueRouter)

const routes = [
  { path: '/login', component: Login, name: 'login' },
  { path: '/password', component: Password },
  { path: '/', component: AccountBeheer },
  { path: '/OtherPage', component: OtherPage }
]

const router = new VueRouter({
  routes
})

export default router
