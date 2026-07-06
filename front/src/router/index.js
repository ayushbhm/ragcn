import { createRouter, createWebHistory } from 'vue-router'

import main from '@/views/main.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/main'
    },
    {
      path: '/main',
      component: main
    }
  ]
})

export default router