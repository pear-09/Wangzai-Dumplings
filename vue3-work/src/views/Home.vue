<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

// 图片数据和逻辑
const images = [
  new URL('@/assets/images1.svg', import.meta.url).href,
  new URL('@/assets/images2.svg', import.meta.url).href,
  new URL('@/assets/images3.svg', import.meta.url).href,
  new URL('@/assets/images4.svg', import.meta.url).href,
  new URL('@/assets/images5.svg', import.meta.url).href,
];

const currentIndex = ref(0);

// 切换到下一张图片
const next = () => {
  currentIndex.value = (currentIndex.value + 1) % images.length;
};

// 切换到上一张图片
const prev = () => {
  currentIndex.value = (currentIndex.value - 1 + images.length) % images.length;
};

// 自动播放功能
let interval: ReturnType<typeof setInterval>;
onMounted(() => {
  interval = setInterval(next, 3000); // 每3秒切换一次
});
onUnmounted(() => {
  clearInterval(interval);
});


// 客户评论数据
const testimonials = [
  {
    name: "Alice Johnson",
    feedback: "EZnote has completely transformed the way I organize my thoughts. It's intuitive and reliable!",
    avatar: new URL('@/assets/avatar1.png', import.meta.url).href,
  },
  {
    name: "Mark Wilson",
    feedback: "I love how simple yet powerful this tool is. Managing my schedule has never been easier.",
    avatar: new URL('@/assets/avatar2.png', import.meta.url).href,
  },
  {
    name: "Sophia Brown",
    feedback: "Great app for productivity! The design is clean, and the features are spot on.",
    avatar: new URL('@/assets/avatar3.png', import.meta.url).href,
  },
];

const currentIndex1 = ref(0);

// 切换到下一条评论
const nextTestimonial = () => {
  currentIndex.value = (currentIndex1.value + 1) % testimonials.length;
};

// 切换到上一条评论
const prevTestimonial = () => {
  currentIndex.value = (currentIndex1.value - 1 + testimonials.length) % testimonials.length;
};
</script>

<template>
    <div>
      <!-- 轮播图部分 -->
      <div class="lunbotu">
        <div class="content">
          <p class="p1">Effortlessly Organize Every Idea</p>
          <p class="p2">Simplify Your Notes</p>
          <button>TRY NOW</button>
        </div>
        <!-- 图片轮播内容 -->
        <img class="images" :src="images[currentIndex]" alt="轮播图" />
        <!-- 左右按钮 -->
        <div class="btn prev" @click="prev">
          <i class="iconfont icon-fangxiang-zuo"></i>
        </div>
        <div class="btn next" @click="next">
          <i class="iconfont icon-fangxiang-you"></i>
        </div>
        <!-- 底部指示器 -->
        <ul class="indicators">
          <li 
            v-for="(image, index) in images" 
            :key="index" 
            :class="{ active: index === currentIndex }"
            @click="currentIndex = index"
          ></li>
        </ul>
        <!-- 装饰图案 -->
        <img class="leaf1" src="../assets/green.svg" alt="">
        <img class="leaf2" src="../assets/green.svg" alt="">
      </div>
  
      <div class="why">
              <!-- 简介模块 -->
      <section class="intro">
        <h2>Why Choose Us?</h2>
        <p>We help you organize your thoughts and ideas with simplicity and ease. Take control of your productivity now!</p>
      </section>
  
      <!-- 卡片模块 -->
      <section class="features">
        <div class="card">
          <img src="../assets/icon1.svg" alt="Feature 1">
          <h3>Easy to Use</h3>
          <p>We help you organize your thoughts and ideas with simplicity and ease. Take control of your productivity now!Our platform is designed for simplicity and user-friendliness.We help you organize your thoughts and ideas with simplicity and ease. Take control of your productivity now!</p>
        </div>
        <div class="card">
          <img src="../assets/icon2.svg" alt="Feature 2">
          <h3>Highly Customizable</h3>
          <p>Adapt the features to meet your unique needs and preferences.</p>
        </div>
        <div class="card">
          <img src="../assets/icon3.svg" alt="Feature 3">
          <h3>Safe & Secure</h3>
          <p>Your data is encrypted and safe with us.</p>
        </div>
      </section>
      </div>
      <!-- <div class="testimonials">
    <h2>What Our Clients Say</h2>
    <div class="testimonial-card">
      <img :src="testimonials[currentIndex].avatar" alt="Avatar" class="avatar" />
      <p class="feedback">"{{ testimonials[currentIndex].feedback }}"</p>
      <p class="client-name">- {{ testimonials[currentIndex].name }}</p>
    </div>


    <div class="testimonial-controls">
      <button @click="prevTestimonial" class="control-btn">Previous</button>
      <button @click="nextTestimonial" class="control-btn">Next</button>
    </div>
  </div> -->
      <!-- 页脚模块 -->
      <footer class="footer">
        <p>&copy; 2024 YourCompany. All rights reserved.</p>
        <div class="social-media">
          <a href="#" class="iconfont icon-facebook"></a>
          <a href="#" class="iconfont icon-twitter"></a>
          <a href="#" class="iconfont icon-instagram"></a>
        </div>
      </footer>
    </div>
    
  </template>
  
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
.lunbotu {
    width: 100%;
    height: 600px;
    display: flex;
    align-items: center;
    position: relative;
    /* background-color: antiquewhite; */
    overflow: hidden;
}
.lunbotu .content {
    width: 40%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    /* align-items: end; */
    padding-left: 150px;
    /* background-color: aquamarine; */
}

.lunbotu .content .p1{
    font-size: 18px;
    color: rgb(87, 81, 81);
    margin-bottom: 15px;
}

.lunbotu .content .p2{
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 20px;
}

.lunbotu .content button{
    width: 190px;
    height: 60px;
    font-weight: 700;
    font-size: 20px;
    border: none;
    border-radius: 8px;
    color: #fff;
    /* background-color: #008e40; */
    background-color: #85ba92;
}

.lunbotu .content button:hover{
    /* background-color: #005a2e; */
    background-color: #638a6c;
    transform: scale(1.05);
    transition:0.3s ease;
}

/* 左右按钮 */
.lunbotu .btn {
  width: 40px;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 50%;
  background-color: #fdfffc;
  box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
  cursor: pointer;
  z-index: 10;
}

.lunbotu .btn:hover{
  background-color: #e5e7e3cd;
  transform: scale(1.05);
  transition: all .3s ease;
}

.lunbotu .prev{
    left:18px
}
.lunbotu .next{
    right: 18px;
}
.lunbotu i{
    font-weight: 600;
}

.lunbotu .images{
    width: 500px;
    height: 400px;
    margin: auto;
    object-fit: cover;
    transition: opacity 0.5s ease;
}

.lunbotu .images:hover{
  transform: scale(1.1);
  transition: all 0.5s ease;
}

/* 底部指示器 */
.lunbotu .indicators {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
}

.lunbotu .indicators li {
  width: 12px;
  height: 12px;
  background-color: rgba(25, 24, 24, 0.5);
  border-radius: 50%;
  cursor: pointer;
  transform: translateY(18px);
}

.lunbotu .indicators li.active {
  background-color: #719e8d;
}

.lunbotu .leaf1{
    width: 100px;
    height: 100px;
    position: absolute;
    bottom: 25px;
    left: 20px;
    transform: rotate(95deg) scale(2); /* 顺时针旋转90度 */

}

.lunbotu .leaf2{
    width: 100px;
    height: 100px;
    position: absolute;
    right: -15px;
    top: 15px;
    transform: scale(1.5) rotate(280deg);
}
.why{
    background-color: #719e8e;
}
/* 简介模块 */
.why .intro {
  text-align: center;
  margin: 40px 20px;
  font-family: Arial, sans-serif;
}

.why .intro h2 {
  font-size: 36px;
  color: #fff;
  /* margin-top: 0px; */
  padding-top: 60px ;
  margin-bottom: 30px;
}

.why .intro p {
  font-size: 20px;
  color: #555;
  line-height: 1.5;
}

/* 卡片模块 */
.why .features {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin: 40px 20px;
}

.why .features .card {
  width: 300px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  padding: 20px;
  margin-bottom: 40px;
}

.why .features .card img {
  width: 60px;
  height: 60px;
  margin-bottom: 15px;
}

.why .features .card h3 {
  font-size: 20px;
  color: #638a6c;
  margin-bottom: 10px;
}

.why .features .card p {
  font-size: 14px;
  color: #555;
}

/* 页脚模块 */
.footer {
  background-color: #638a6c;
  color: white;
  text-align: center;
  padding: 20px 10px;
  margin-top: 40px;
}

.footer .social-media a {
  color: white;
  font-size: 20px;
  margin: 0 10px;
  transition: color 0.3s ease;
}

.footer .social-media a:hover {
  color: #85ba92;
}
.testimonials {
  text-align: center;
  padding: 50px 20px;
  /* background-color: #85ba92; */
  /* border-top: 2px solid #e0e0e0; */
}

.testimonials h2 {
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
}

.testimonial-card {
  max-width: 600px;
  margin: 0 auto;
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.testimonial-card .avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 15px;
}

.testimonial-card .feedback {
  font-size: 18px;
  color: #555;
  margin-bottom: 10px;
  line-height: 1.6;
}

.testimonial-card .client-name {
  font-size: 16px;
  color: #888;
  font-weight: bold;
}

.testimonial-controls {
  margin-top: 20px;
}

.control-btn {
  background-color: #85ba92;
  color: white;
  font-size: 16px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 0 10px;
  transition: background-color 0.3s ease;
}

.control-btn:hover {
  background-color: #638a6c;
}
</style>
