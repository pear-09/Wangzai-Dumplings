import Home from '@/views/Home.vue'
import Land from '@/views/Land.vue'
import Note from '@/views/Note.vue'
import NoteDetail from '@/views/NoteDetail.vue'
import NoteFile from '@/views/NoteFile.vue'
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
      name:'bjwjj',
      path:'/notefile',
      component:NoteFile

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
  {
    name: 'biji',
    path: '/note/:id',
    component: Note
  },
  {
    name: 'noteDetail',
    path: '/noteDetail/:id',
    component: NoteDetail,
    props: true, // 启用 props 将路由参数传递给组件
  },
  {
    path: '/noteDetail/new',  // 新建笔记的路径
    name: 'newNote',
    component: NoteDetail,  // 使用同样的 NoteDetail 组件来处理新建和编辑
  }

  ],
})

export default router
