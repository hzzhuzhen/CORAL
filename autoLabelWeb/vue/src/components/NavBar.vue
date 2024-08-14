<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light nav-color">
    <div class="container">
      <router-link class="navbar-brand" :to="{ name: 'home' }">FreeAL</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText"
        aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarText">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link " :to="{ name: 'home' }">页面1</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'trackboard' }">页面2</router-link>
          </li>
          <!--<li class="nav-item">
          <router-link class="nav-link" :to="{name:'userprofile',params:{userId:1}}">用户动态</router-link>
        </li>-->
        </ul>
        <!--取反，如果未登录展示登录与注册-->
        <ul class="navbar-nav " v-if="!$store.state.user.is_login">
          <li class="nav-item">
            <router-link class="nav-link " :to="{ name: 'login' }">登录</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link">|</a>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'register' }">注册</router-link>
          </li>
        </ul>
        <!--登录成功显示姓名和退出，并转到登录界面-->
        <ul class="navbar-nav " v-else>
          <li class="nav-item">
            <!--<router-link class="nav-link " :to="{name:'userprofile',params:{userId:$store.state.user.id}}">{{$store.state.user.username}}</router-link>-->
            <router-link class="nav-link " :to="{ name: 'userprofile', params: { userId: $store.state.user.id } }">{{
              $store.state.user.username }}</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link">|</a>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'login' }" style="cursor: pointer;"
              @click="logout">退出</router-link>
          </li>
        </ul>

      </div>
    </div>
  </nav>
</template>

<script>
import { useStore } from 'vuex';
export default {
  name: "NavBar",
  //退出删除掉jwt的事件
  setup() {
    const store = useStore();
    const logout = () => {
      store.commit('logout');
    };
    return {
      logout,
    }
  }

}
</script>

<style scoped>
.nav-color {
  background-color: rgb(38, 38, 38);
}
</style>