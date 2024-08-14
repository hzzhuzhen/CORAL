<template>
  <div class="card">
    <div class="card-body">
      <div class="row">
        <div class="col-3 img-field">
          <img class="img-fluid" :src="user.photo" alt="">
        </div>
        <div class="col-9">
          <div class="username">{{ user.username }}</div>
          <div class="fans,fw-lighter">粉丝数:{{ user.followerCount }}</div>
          <div>
            <button @click="follow" v-if="!user.is_followed" type="button" class="btn btn-primary btn-sm">+关注</button>
            <button @click="unfollow" v-if="user.is_followed" type="button" class="btn btn-primary btn-sm">取消关注
            </button>
            <button type="button" class="btn btn-danger btn-sm">发消息</button>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>
<script>
//import {computed} from 'vue';

import $ from 'jquery';
import {useStore} from 'vuex';

export default {
  name: 'UserProfileInfo',
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  setup(props, context) {
    const store = useStore();
    //let fullName=computed(()=>props.user.lastName+' '+props.user.firstName);
    const follow = () => {
      //更新数据库状态
      $.ajax({
        url: "https://app165.acapp.acwing.com.cn/myspace/follow/",
        type: "POST",
        data: {
          target_id: props.user.id,//当前用户id

        },
        headers: {
          //Authorication,//身份验证
          'Authorization': 'Bearer ' + store.state.user.access, //授权

        },
        success(resp) {
          if (resp.result === "success") {
            //授权成功之后则在前端渲染
            // console.log("follow",resp);
            context.emit("follow");

          }


        }

      });

    };
    const unfollow = () => {
      //更新数据库状态
      $.ajax({
        url: "https://app165.acapp.acwing.com.cn/myspace/follow/",
        type: "POST",
        data: {
          target_id: props.user.id,//当前用户id

        },
        headers: {
          //Authorization,身份验证
          'Authorization': 'Bearer ' + store.state.user.access, //授权

        },
        success(resp) {
          //授权成功之后则在前端渲染
          if (resp.result === "success") {
            //console.log("unfollow",resp);
            context.emit("unfollow");

          }


        }

      });


    };
    return {
      // fullName,
      follow,
      unfollow,
    }

  }
}
</script>
<style scoped>
img {
  border-radius: 50%;
  /*width:30px;
  height:50px;*/
}

.username {
  font-weight: bold;
  font-size: 15px;

}

.fans {
  font-size: 12px;
  color: grey;
}

button {
  padding: 2px, 4px;
  font-size: 12px;
}

.card-body {
  background-color: lightblue;
  padding: 2px, 4px;
  font-size: 12px;

}

.img-field {
  display: flex;
  flex-direction: column;
  justify-content: center;


}

</style>