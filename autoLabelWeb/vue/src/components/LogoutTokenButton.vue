<template>
  <button @click="logoutToken">logoutToken</button>
</template>

<script setup>
import Cookies from "js-cookie";
const logoutToken=()=>{
  Cookies.remove('token');
  alert("删除token成功");
}
</script>

<style scoped>

</style>