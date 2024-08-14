<template>
 
<ContentBase>
    好友列表
    <div class="card" v-for="user in users" :key="user.id" @click="open_user_profile(user.id)"><!--传入的应为user.id-->
      <div class="card-body">
        <div class="row">
          <div class="col-1 img-field">
                <img class="img-fluid" :src="user.photo" alt="">
          </div>
          <div class="col-11">
            <!--用户名和粉丝数量-->            
            <div class="username fw-blod">姓名：{{user.username}}</div>
            <div class="follower-count">粉丝数:{{user.followerCount}}</div>
          </div>
        </div>
      </div>
    </div>

</ContentBase>

</template>

<script>

import ContentBase from '../components/ContentBase';
import $ from 'jquery';
import {ref} from 'vue';
import router from '@/router/index';
import { useStore } from 'vuex';//判断是否登录

export default {
  name: 'UserList',
  components: {
    ContentBase,
  },
  setup(){
    const store=useStore();
    let users=ref([]);//变量初始为空
    //云端动态获取用户信息
    $.ajax({
      url:'https://app165.acapp.acwing.com.cn/myspace/userlist/',
      type:'get',
      success(resp){
        //console.log(resp);
        users.value=resp;
      }
    });
    //当点击用户进入相应的用户动态页面
    const open_user_profile=userId=>{
      //判断是否登录
      if(store.state.user.is_login){
        //已经登录，跳转到userproflie页面
        router.push({
          name:'userprofile',
          //注意是params
          params:{
            userId:userId,

          }
        })
      }else{
        //未登录跳转到登录页面
        router.push({
          name:'login',

        });
      }

    }


    return{
      users,
      open_user_profile,

    }

  }
}
</script>
<style scoped>
img{
  border-radius: 50%;
}
.username{
  font-size:20px;
  height:50%;

}
.follower-count{
  font-size:12px;
  color:gray;
  height:50%;
}
.card{
  margin-bottom:10px;
  cursor:pointer;
}
.card:hover{
  box-shadow: 2px 2px 10px lightgrey;
  transition: 500ms;
}
.img-field{
    display:flex;
    flex-direction:column;
    justify-content: center;

}
</style>