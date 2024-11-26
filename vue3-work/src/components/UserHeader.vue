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
            <i class="iconfont icon-sousuo"></i>
            <i class="iconfont icon-tixing1"></i>
            <i class="iconfont icon-yonghu" @click="toggleLogout"></i>
  
            <!-- 点击头像图标时显示退出按钮 -->
            <div v-if="showLogout" class="logout-button" @click="logout">
              退出登录
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 展示区 -->
    <RouterView />
  </template>
  
  <script lang="ts">
  import { RouterView, RouterLink } from 'vue-router';
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';  // 用于页面跳转
  import axios from 'axios';  // 用于发送请求
  
  export default {
    name: 'UserHeader',
    setup() {
      // 使用 ref 来管理状态
      const isLoggedIn = ref(false); // 默认未登录
      const showLogout = ref(false); // 控制退出按钮显示
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
  
      return {
        isLoggedIn,
        showLogout,
        loggedInUsername,
        toggleLogout,
        logout,
        login,
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

.iconfont {
  font-size: 20px;
  cursor: pointer;
}

.iconfont:hover {
  color: #007bff;
}
</style>
