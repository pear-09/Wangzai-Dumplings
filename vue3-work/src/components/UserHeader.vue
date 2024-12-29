<template>
  <!-- 导航栏 -->
  <div id="app">
    <div class="UserHeader">
      <div class="logo">
        EZnote
      </div>
      <div class="navy">
        <ul>
          <li><RouterLink to="/home" active-class="active">首页</RouterLink></li>
          <li><RouterLink to="/notefile" active-class="active">笔记</RouterLink></li>
          <li><RouterLink to="/schedule" active-class="active">日程</RouterLink></li>
          <li><RouterLink to="/write" active-class="active">写作</RouterLink></li>
          <li v-if="!isLoggedIn"><RouterLink to="/land" active-class="active">登录</RouterLink></li>
        </ul>
        <div class="tubiao" v-if="isLoggedIn">
          <i class="iconfont icon-sousuo" @click="toggleSidebar"></i>
          <i class="iconfont icon-tixing1"></i>
          <i class="iconfont icon-yonghu" @click="toggleLogout"></i>
          <div v-if="showLogout" class="logout-button" @click="logout">
            退出登录
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 侧边栏 -->
  <div v-if="showSidebar" class="sidebar">
    <div class="search-wrapper">
      <i class="iconfont icon-sousuo"></i>
      <input v-model="searchQuery" @input="searchProjects" placeholder="搜索项目..." />
      <i v-if="searchQuery" class="iconfont icon-close" @click="clearSearch"></i>
    </div>
    <div v-if="searchResults.length > 0">
      <ul>
        <li v-for="result in searchResults" :key="result.id" @click="goToNoteDetail(result)">
          {{ result.title }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>没有找到相关笔记。</p>
    </div>
    <button class="close-sidebar" @click="toggleSidebar">×</button>
  </div>

  <!-- 展示区 -->
  <RouterView />
</template>


<script lang="ts">
  import { RouterView, RouterLink } from 'vue-router';
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';  // 用于页面跳转
  import axios from 'axios';  // 用于发送请求
  import request from '@/utils/request'; // 导入 request 实例

  export default {
    name: 'UserHeader',
    setup() {
      // 使用 ref 来管理状态
      const isLoggedIn = ref(false); // 默认未登录
      const showLogout = ref(false); // 控制退出按钮显示
      const showSidebar = ref(false); // 侧边栏的显示状态
      const searchQuery = ref(''); // 搜索框的内容
      const searchResults = ref([]); // 搜索结果列表
      const loggedInUsername = ref('');  // 存储已登录的用户名
      const router = useRouter(); // 用 router 实例进行页面跳转

      // 页面加载时检查 localStorage，判断用户是否登录
      onMounted(() => {
        const storedUsername = localStorage.getItem('username');
        const token = localStorage.getItem('auth_token');
        if (storedUsername && token) {
          loggedInUsername.value = storedUsername;
          isLoggedIn.value = true;
        }
      });

      // 切换退出按钮显示
      const toggleLogout = () => {
        showLogout.value = !showLogout.value;
      };

      // 登出方法
      const logout = () => {
        localStorage.removeItem('username');
        localStorage.removeItem('auth_token');
        loggedInUsername.value = '';
        isLoggedIn.value = false;
        showLogout.value = false; // 隐藏退出登录按钮
      };

      // 登录方法
      const login = async (username: string, password: string) => {
        try {
          const response = await axios.post(`${import.meta.env.VITE_API_URL}/ez-note/user/login`, 
            {
              username, 
              password
            }, 
            {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
              }
            }
          );
          
          if (response.data.code === 0) {
            // 登录成功
            localStorage.setItem('auth_token', response.data.token || '');
            localStorage.setItem('username', username);
            loggedInUsername.value = username;
            isLoggedIn.value = true;

            alert('登录成功');
            router.push('/home');  // 跳转到主页
          } else {
            console.error(response.data.msg || '登录失败，请稍后再试');
          }
        } catch (error) {
          console.error('登录失败:', error);
        }
      };

      // 控制侧边栏显示/隐藏
      const toggleSidebar = () => {
        showSidebar.value = !showSidebar.value;
      };

      // 实时搜索项目
      const searchProjects = async () => {
        if (searchQuery.value.trim() === '') {
          searchResults.value = [];
          return;
        }
        try {
          const response = await request.get('/ez-note/note/search', {
            params: { tag: searchQuery.value }
          });
          if (response.code === 0) {
            // 从后端返回的数据中提取笔记标题
            searchResults.value = response.data.notes.map(note => ({
              id: note.id,
              title: note.title,
              folder_id: note.folder_id // 保留 folder_id
            }));
          } else {
            console.error('搜索失败');
            searchResults.value = [];
          }
        } catch (error) {
          console.error('搜索请求失败:', error);
          searchResults.value = [];
        }
      };

      // 点击笔记标题跳转到笔记详情页
      const goToNoteDetail = (note) => {
        router.push({
          name: 'noteDetail',
          params: {
            folder_id: note.folder_id,
            id: note.id,
            title: note.title
          }
        });
      };

      return {
        isLoggedIn,
        showLogout,
        loggedInUsername,
        showSidebar,
        searchQuery,
        searchResults,
        toggleLogout,
        logout,
        login,
        toggleSidebar,
        searchProjects,
        goToNoteDetail
      };
    },
  };
</script>


  

<style scoped>
*{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
li{
    list-style: none;
    border: none;
}
a{
    text-decoration: none;
    border: none;
}
body {
  width: 100%;
  background-color: #f8f7f4 !important;
}

#app .UserHeader{
    width: 100%;
    height: 90px;
    display: flex;
    justify-content: space-between;
    background-color:#fdfffc;
    box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
    margin-bottom: 15px;
}

#app .UserHeader .logo{
    width:600px;

    height: 100%;
    padding: 0 20px;
    margin-left: 10px;
    color: #0d0c21;
    margin-top: 10px;
    font-size: 28px;
    /* font-weight: 800; */
    /* letter-spacing: 3px; */
    /* font-family: 'Permanent Marker', cursive; */
    font-family: 'Kaushan Script', cursive;
}

#app .UserHeader .navy{
    width: 100%;
    height: 60px;
    display: flex;
    justify-content:flex-end;
    align-items: end;
    margin-top: 10px;
    border-radius: 5px;
    /* background-color:bisque; */
}

#app .UserHeader .navy ul li{
    display: inline-block;
    /* font-weight:500; */
    margin-right: 50px;
}

#app .UserHeader .navy ul li a{
    position: relative;
    font-size: 18px;
    color: #0d0c21;
    z-index: 2;
}

#app .UserHeader .navy a::after{
    content: ' ';
    position: absolute;
    top: 100%;
    left: 50%;
    width: 120%;
    height: 80%;
    padding: 11px 15px;
    border-radius: 50px;
    background-color:#759a8b;
    transform: translate(-50%,-50%);
    z-index: -1;
    opacity: 0;
}

#app .UserHeader .navy a.active::after{
    top:50%;
    opacity: 1;
}

#app .UserHeader .navy a.active{
    color: #fff;
}

#app .UserHeader .navy li a:hover{
    color: #fff;
}


#app .UserHeader .navy li a:hover::after{
    top:50%;
    opacity: 1;
    transition: all .4s;
}

.navy .tubiao{
    margin-left: 50px;
}

.navy .tubiao i{
    font-size: 24px;
    /* padding: 0 5px; */
    margin-right: 15px;
}
/* 样式：控制退出登录按钮的显示和位置 */
.tubiao {
  position: relative;
}

.logout-button {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #f0f0f0;
  padding: 5px 10px;
  border: 1px solid #ddd;
  cursor: pointer;
  font-size: 14px;
  color: #333;
  border-radius: 5px;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
  display: inline-block;
}

.logout-button:hover {
  background-color: #e0e0e0;
}

/* .iconfont {
  font-size: 20px;
  cursor: pointer;
}

.iconfont:hover {
  color: #007bff;
} */

/* Sidebar Section */
/* 侧边栏 */
.sidebar {
  position: absolute;
  top: 102px;
  right: 8px;
  width: 300px; /* 侧边栏宽度 */
  height: calc(100vh - 102px);
  background-color: #fdfffc;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  z-index: 1000;
  border-radius: 8px 0 0 8px;
}

/* 搜索框样式 */
.sidebar .search-wrapper {
  position: relative;
  width: 100%;
  margin-bottom: 15px;
}

.sidebar input {
  margin-top: 30px;
  width: 100%;
  padding: 12px;
  padding-left: 40px;
  font-size: 16px;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.sidebar .iconfont.icon-sousuo {
  position: absolute;
  left: 12px;
  top: 70%;
  transform: translateY(-50%);
  font-size: 20px;
  color: #aaa;
}

.sidebar .iconfont.icon-close {
  position: absolute;
  right: 12px;
  top: -10px;
  transform: translateY(-50%);
  font-size: 20px;
  color: #aaa;
  cursor: pointer;
}

/* 搜索结果项样式 */
.sidebar ul {
  list-style: none;
  padding: 0;
  width: 100%;  /* 使ul宽度为100% */
}

.sidebar li {
  padding: 12px 15px;
  margin-bottom: 10px;
  font-size: 16px;
  color: #333;
  background-color: #f9f9f9;
  border-radius: 10px; /* 圆角效果 */
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);  /* 阴影效果 */
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%; /* 保证宽度为100%，与侧边栏宽度一致 */
}

.sidebar li:hover {
  background-color: #759a8b;  /* 鼠标悬停时改变背景色 */
  color: #fff;  /* 文本颜色为白色 */
}

.sidebar li.active {
  background-color: #759a8b;
  color: #fff;
  font-weight: bold;
}

/* 关闭侧边栏按钮 */
.sidebar .close-sidebar {
  position: absolute;
  top: 20px;
  right: 10px;
  background: none;
  border: none;
  font-size: 30px;
  color: #759a8b;
  cursor: pointer;
}

.sidebar .close-sidebar:hover {
  color: #d9534f;
}


/* Icon Button Style */
.iconfont {
    font-size: 24px;
    cursor: pointer;
}

.iconfont:hover {
    color: #759a8b;
}
</style>
