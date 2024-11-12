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

<style scoped>

</style>
