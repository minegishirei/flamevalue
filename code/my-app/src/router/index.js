import { createRouter, createWebHistory } from 'vue-router'
import MyTemplate from '../components/templates/template'

const routes = [
  {
    path: '/',
    name: 'MyTemplate',
    component: MyTemplate
  }
]

const router = createRouter({
  mode: "hash",
  history: createWebHistory("/github-pages.beaver/"),
  routes
})


export default router
