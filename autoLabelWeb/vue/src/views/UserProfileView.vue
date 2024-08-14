<template>
 
<ContentBase>
    <div class="row">
      <div class="col-3">
        <UserProfileInfo @follow="follow" @unfollow="unfollow" :user="user"/>
        <!--如果是自己才显示编辑模块-->
        <UserProfileWrite v-if="is_me" @post_a_post="post_a_post"/>
      </div>
        <div class="col-9">帖子列表
          <!--将user和posts传进来-->
          <UserProfilePosts :user="user" :posts="posts" @delete_a_post="delete_a_post"/>
        </div>
    </div>

</ContentBase>

</template>

<script>

import ContentBase from '../components/ContentBase';
import UserProfileInfo from '../components/UserProfileInfo';
import UserProfilePosts from '../components/UserProfilePosts';
import UserProfileWrite from '../components/UserProfileWrite';
import {reactive} from 'vue';
import { useRoute } from 'vue-router';
import $ from 'jquery';
import { useStore } from 'vuex';
import {computed} from 'vue';


export default {
  name: 'UserProfile',
  components: {
    ContentBase,
    UserProfileInfo,
    UserProfilePosts,
    UserProfileWrite,


  },
  setup(){
    const store=useStore();

    const route=useRoute();
    const userId=parseInt(route.params.userId);
   // console.log(userId);
   //user 一般不会变，可以用reactive
    const user=reactive({
     /* id:1,
      username:"小米汽车",
      lastName:"小米",
      firstName:"汽车",
      followerCount:"100",
      is_followed:false,//是否关注,false:未关注，true：已关注*/


    });
    const posts=reactive({
      /*count:3,//帖子数量
      posts:[
        {
          id:1,
          userId:1,
          content:"小米12s系列，徕卡影像，7月4日见"

        },
        {
          id:2,
          userId:1,
          content:"小米手环7Pro，时尚新选择，7月4日见"

        },
        {
          id:3,
          userId:1,
          content:"小米汽车c1，性价比轿跑，7月4日见"

        },






      ]*/

    });
    $.ajax({
      url:"https://app165.acapp.acwing.com.cn/myspace/getinfo/",
      type:"GET",
      data:{
        user_id:userId,

      },
      headers:{
        'Authorization': "Bearer " +store.state.user.access,
      },
      success(resp){
        user.id=resp.id;
        user.username=resp.username;
        user.photo=resp.photo;
        user.followerCount=resp.followerCount;
        user.is_followed=resp.is_followed;//指的是当前登录的用户是否关注当前正在看的用户
        //console.log(resp);
      },
      error(){
        console.log("failed");
      }


    });
    $.ajax({
      url:"https://app165.acapp.acwing.com.cn/myspace/post/",
      type:"GET",
      data:{
        user_id:userId
      },
      headers:{
        'Authorization': "Bearer " +store.state.user.access,
      },
      success(resp){
        posts.count=resp.length;
        posts.posts=resp;
        //console.log(resp);
      },
      error(){
        console.log("failed");
      }


    });
    const follow=()=>{
      if(user.is_followed)return;//已经关注就无需重复关注
      user.is_followed=true;
      user.followerCount++;

    };
    const unfollow=()=>{
      if(!user.is_followed)return;//已经取消关注就无需取消关注
      user.is_followed=false;//否则取消关注并且关注数减一
      user.followerCount--;

    };
    //发布一个帖子
    const post_a_post=(content)=>{
      posts.count++;
      posts.posts.unshift({
        id:posts.count,
        userId:1,
        content:content,
      })
    };
    //删除一个帖子
    const delete_a_post=(post_id)=>{
      posts.posts=posts.posts.filter(posts=>posts.id!=post_id);//过滤，判断该元素是否应该被保留下来
      posts.count=posts.posts.length;



    };
    /*const change_a_post=(post_id)=>{

    };*/

    //判断当前页面是不是自己
    //console.log(typeof(userId),typeof(store.state.user.id));
    const is_me=computed(()=>userId===store.state.user.id);
    return {
      user,
      follow,
      unfollow,
      posts,
      post_a_post,
      delete_a_post,
      is_me,

    }
  }
}
</script>
<style scoped>

</style>