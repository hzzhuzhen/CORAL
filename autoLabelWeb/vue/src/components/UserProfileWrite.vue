<template>
    <div class="card edit-field">
        <div class="card-body">
           <div class="mb-3">
          <label for="edit-post" class="form-label">请在这里写下你的新鲜事</label>
          <textarea v-model="content" class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
          <button @click="post_a_post" type="button" class="btn btn-success edit-submit btn-sm">提交</button>
       </div>
     </div>
    </div>
</template>
<script>
import { ref } from 'vue';
import $ from 'jquery';
import { useStore } from 'vuex';
export default {
    name:'UserProfileWrite',
    setup(prpos,context){
        const store=useStore();
        let content=ref('');

        const post_a_post=()=>{
            $.ajax({
                url:"https://app165.acapp.acwing.com.cn/myspace/post/",
                type:"POST",
                data:{
                    content:content.value,
                },
                headers:{
                   'Authorization': "Bearer " +store.state.user.access,
                },
                success(resp){
                    //api授权为success，则在前端改掉
                    if(resp.result==="success"){
                          context.emit("post_a_post",content.value);
                         // console.log(content.value);
                          content.value="";

                    }
                }
            })
          
        }

        return {
            content:content,
            post_a_post
        }
    }
}
</script>
<style scoped>
.edit-field{
    margin-top:10px;
    width:210px;

}
.edit-submit{
    margin-top:10px;

}
</style>