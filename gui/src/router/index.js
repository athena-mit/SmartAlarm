import { createRouter, createWebHistory } from 'vue-router'
import AlarmView from "@/views/AlarmView.vue";
import CalendarView from "@/views/CalendarView.vue";
import RoomView from "@/views/RoomView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: AlarmView
    },
    {
      path: '/calendar',
      name: 'calendar',
      component: CalendarView
    },
    {
      path: '/room',
      name: 'room',
      component: RoomView
    }
  ]
})

export default router

