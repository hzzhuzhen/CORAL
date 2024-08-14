<template>
  <el-form-item style="margin-left: 150px">
    <!-- Demo按钮 -->
    <el-button type="primary" @click="DemoForm()" style="width: 200px">Demo</el-button>
  </el-form-item>
</template>

<script setup>
import axios from 'axios';
import {useRouter} from 'vue-router';
import Cookies from "js-cookie";
import {inject} from "vue";
//const store = useStore();

//let isRefinery = ref(store.getters.getIsRefinery);
const router = useRouter();

//import {useStore} from "vuex";

let demoApi = inject('demoApi');
const DemoForm = () => {
  //提交任务
  axios
      .get(demoApi.value + "/demo/task/upset")
      .then((response) => {
        console.log("服务器响应:", response.data);
        console.log("taskId:", response.data.data);
        console.log("code:", response.data.code);
        localStorage.setItem('isRefinery', 'false');
        //如果正在运行直接跳过
        if (response.data.code === 201) {
          router.push({path: "/LLMView"});
        } else if (response.data.code === 200) {
          // alert("成功");
          Cookies.set("taskId", response.data.data.taskId);

          //跳转到大模型
          router.push({path: "/LLMView"});
          //跳转到小模型
          // router.push({path: "/SLMView"});
        } else {
          alert(response.data.code + response.data.message);
        }

      })
      .catch((error) => {
        console.error("请求失败:", error);
        alert("请求失败");
        // 在这里处理请求失败的情况，可以提示用户或执行其他操作
      });
}

</script>
<style scoped>

</style>