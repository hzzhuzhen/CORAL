<template>
  <div style="margin-top: 1rem; font-size: 25px;"><strong>LLM Running Progress</strong></div>
  <div style="margin-top: 10px;">
    <div>
      <el-progress type="circle" :percentage="percentage" :color="colors" :width="140"></el-progress>
    </div>
  </div>
</template>

<script setup>
import {inject, onBeforeUnmount, onMounted, ref} from "vue";
import axios from "axios";
import {useStore} from 'vuex';
import Cookies from "js-cookie";
// import { message } from 'ant-design-vue';
// import { confirm } from 'ant-design-vue';

const store = useStore();

let isRefinery = ref(store.getters.getIsRefinery);
let percentage = ref(0);

if (isRefinery.value === true) {
  localStorage.setItem('isRefinery', isRefinery.value);
}
if (localStorage.getItem('isRefinery') !== undefined) {
  isRefinery.value = localStorage.getItem('isRefinery');
}

console.log("isRefinery666=" + isRefinery.value);

const open = () => {
  confirm('异常结束！是否重新进行？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    this.$message({
      type: 'success',
      message: '重新进行!'
    });
  }).catch(() => {
    this.$message({
      type: 'info',
      message: '已取消'
    });
    clearInterval(pollingTimer);
  });
}

const colors = [
  {color: "#f56c6c", percentage: 20},
  {color: "#e6a23c", percentage: 40},
  {color: "#5cb87a", percentage: 60},
  {color: "#1989fa", percentage: 80},
  {color: "#6f7ad3", percentage: 100},
];
//const taskId = getCookieValue('taskId');
const taskId = Cookies.get('taskId');
let pollingTimer = null;

let demoApi = inject('demoApi');
const pollDataFromBackend = () => {
  axios.get(demoApi.value + "/demo/progress/llm/check", {
    params: {
      taskId: taskId,
      isRefinery: isRefinery.value
    }
  })
      .then((response) => {
        if (response.data.code === 200) {
          const status = response.data.data.status;
          const total = response.data.data.total;
          const current = response.data.data.current;
          store.dispatch('setStatus', status);
          store.dispatch('setTotal', total);
          store.dispatch('setCurrent', current);
          console.log("currentLLM=" + current);
          console.log("status=" + status);

          //读取进度条
          const confidencePercentage = (parseFloat(current * 1.0 / total) * 100).toFixed(2);
          console.log("confidencePercentage=" + confidencePercentage);
          percentage.value = Math.min(parseFloat(confidencePercentage), 100);

          if (status === 'finish') {
            if (response.data.data.exit === 1) {
              clearInterval(pollingTimer);
              open();
            }
            clearInterval(pollingTimer);
            console.log("任务已完成");
          }
        } else {
          //alert(response.data.code + response.data.message);
        }
      })
      .catch((error) => {
        console.error("请求失败:", error);
        //alert("请求失败llm");
        //clearInterval(pollingTimer);
      });
};

onMounted(() => {
  //pollDataFromBackend();
  //setTimeout(() => {
  pollingTimer = setInterval(pollDataFromBackend, 2000);
  store.dispatch('setTaskId', taskId);
  // }, 5000);

});

onBeforeUnmount(() => {
  clearInterval(pollingTimer);
});


</script>

<style scoped>
</style>
