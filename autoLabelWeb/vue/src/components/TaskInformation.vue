<template>
  <div style="text-align: center; font-size: 25px;">
    <strong>Task Information</strong>
  </div>
  <div style=" margin-top: 1rem;">
    <div
        style="text-align: left; display: flex; flex-direction: column; justify-content: center; margin-left: 22%;">
      <p><span style="color: rgb(246,103,11);">Task Name: </span>{{ taskName }}</p>
      <p><span style="color: rgb(246,103,11);">LLM Model: </span>{{ llmModel }}</p>
      <p><span style="color: rgb(246,103,11);">SLM Model: </span>{{ slmModel }}</p>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import {onMounted, ref} from "vue";
import Cookies from "js-cookie";

//基本任务信息存放变量
let llmModel = ref('');
let taskName = ref('');
let slmModel = ref('');

// 请求基础任务数据
const askForBasicTaskInfo = () => {
  axios
      .get('http://localhost:8082/task/basicInfo', {
        params: {
          taskId: Cookies.get('taskId')
        }
      })
      .then(response => {
        taskName.value = response.data.data.taskName
        llmModel.value = response.data.data.llmModel
        slmModel.value = response.data.data.slmModel
      })
      .catch(error => {
        console.error(error)
      })
}

onMounted(() => {
  askForBasicTaskInfo()
})
</script>

<style scoped>

</style>