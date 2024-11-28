import Home from '@/views/Home.vue'
import Land from '@/views/Land.vue'
import NoteDetail from '@/views/NoteDetail.vue'
import NoteFile from '@/views/NoteFile.vue'
import Register from '@/views/Register.vue'
import Schedule from '@/views/Schedule.vue'
import Write from '@/views/Write.vue'
import WriteEdit from '@/views/WriteEdit.vue'
import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Home
    },
    {
      path: '/home',
      component: Home,
    },
    {
      name: 'bjwjj',
      path: '/notefile',
      component: NoteFile

    },
    {
      name: 'richeng',
      path: '/schedule',
      component: Schedule
    },
    {
      name: 'xiezuo',
      path: '/write',
      component: Write
    },
    {
      path: '/write-edit:id?',
      name: 'writeEdit',
      component: WriteEdit,
      props: true, // 传递路由参数作为 prop 给组件
    },
    {
      name: 'denglu',
      path: '/land',
      component: Land
    },
    {
      name: 'zhuce',
      path: '/register',
      component: Register
    },
    // {
    //   name: 'biji',
    //   path: '/note/:id',
    //   component: NoteDetail,  // 跳转到 NoteDetail 页面
    //   props: true,  // 启用 props 将路由参数传递给组件
    // },
    {
      name: 'noteDetail',
      path: '/note/:folder_id/:id?/:title?',  // 路径包含 folder_id 和可选的 id
      component: NoteDetail,
      props: (route) => ({
        folderId: Number(route.params.folder_id), // 确保 folderId 是数字
        id: route.params.id || 'new', // 如果 id 不存在，则默认为 'new'
        title: route.params.title || '新建笔记',  // 默认标题
      }),
    },

  ],
})

export default router
