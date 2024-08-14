<template>
    <div class="card" >
        <div class="card-body ">
          <div v-for="post in posts.posts" :key="post.id" >
              <div class="card single-post ">
                <div class="card-body card-color">
                    {{post.content}}
                    <!--<button @click="change_a_post(post.id)" v-if="is_me" type="button" class="btn btn-success btn-sm btn-change">修改</button>-->
                    <button  v-if="is_me" type="button" class="btn btn-success btn-sm btn-change">修改</button>
                     <button @click="delete_a_post(post.id)" v-if="is_me" type="button" class="btn btn-danger btn-delete btn-sm">删除</button>
                  </div>
              </div>
            
           </div>
        </div>
    </div>
</template>
<script>
import {computed} from 'vue';
import {useStore} from 'vuex';
import $ from 'jquery';

export default{
    name:'UserProfilePosts',
    props:{
        posts:{
            type:Object,
            required:true,
    
        },
        user:{
             type:Object,
            required:true,
        },
    },
    setup(props,context){
        const store=useStore();
        let is_me=computed(()=>store.state.user.id===props.user.id);
        /*const change_a_post=(post_id)=>{
            $.ajax({
                url:"https://app165.acapp.acwing.com.cn/myspace/post/",
                type:"PUT",
                data:{
                    post_id,
                },
                headers:{
                    'Authorization':"Bearer " +store.state.user.access,
                },
                success(resp){
                    console.log()
                }

            });
        }*/
        //删除帖子
        const delete_a_post=(post_id)=>{
            $.ajax({
                url:"https://app165.acapp.acwing.com.cn/myspace/post/",
                type:"DELETE",
                data:{
                    post_id,

                },
                headers:{
                    'Authorization': 'Bearer ' +store.state.user.access, //身份验证
                },
                success(resp){
                    if(resp.result==="success"){
                        //后端操作成功，则前端显示实现真正删掉
                         context.emit('delete_a_post',post_id);

                    }
                    //console.log(resp);
                },error(){
                    //console.log("failed");
                }



            });

        }
        return {
            is_me,
            delete_a_post,
            //change_a_post,
        }
    }
}  
</script>
<style scoped>
.single-post{
    margin-bottom: 10px;
    background-color:lightgreen;
 
}

.btn-delete{
    font-size:12px;
    color:white;
    padding:2px,2px;
    float:right;

}
.btn-change{
    font-size:12px;
    padding:2px,2px;
    float:right;
}

/*div.card-color:nth-child(odd){
    background-color:lightcoral;
}
div.card-color:nth-child(even){
    background-color:lightblue;


}*/

</style>