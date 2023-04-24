import { createRouter, createWebHistory } from 'vue-router'
import AlarmView from "@/views/AlarmView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: AlarmView
    }
  ]
})

export default router

