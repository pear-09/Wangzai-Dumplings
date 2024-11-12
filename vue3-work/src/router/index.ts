import Home from '@/views/Home.vue'
import Land from '@/views/Land.vue'
import Note from '@/views/Note.vue'
import Register from '@/views/Register.vue'
import Schedule from '@/views/Schedule.vue'
import Write from '@/views/Write.vue'
import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
  {
      path:'/',
      component:Home
  },
  {
      path:'/home',
      component:Home,
  },
  {
      name:'biji',
      path:'/note',
      component:Note
  },
  {
      name:'richeng',
      path:'/schedule',
      component:Schedule
  },
  {
      name:'xiezuo',
      path:'/write',
      component:Write
  },
  {
    name:'denglu',
    path:'/land',
    component:Land
  },
  {
    name:'zhuce',
    path:'/register',
    component:Register
  },

  ],
})

export default router
