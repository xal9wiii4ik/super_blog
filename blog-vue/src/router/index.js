import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/posts',
    name: 'posts',
    component: () => import('@/views/posts')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
