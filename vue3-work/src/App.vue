<template>
  <UserHeader />
</template>

<script lang="ts">
import UserHeader from "./components/UserHeader.vue";
import request from "./utils/request.ts"
  export default {
    name:'App',
    components:{UserHeader}
  }
</script>

<style>
html, body {
  /* margin: 0;
  padding: 0; */
  height: 100%;
  background-color: #fdfffc /* 设置背景颜色 */
}
</style>
