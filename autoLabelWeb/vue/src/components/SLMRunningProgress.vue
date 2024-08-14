<template>

  <div style="margin-top: 2px; font-size: 25px;"><strong>SLM Running Progress</strong></div>
  <div style="margin-top: 15px; font-size: 25px;">
    <div style="text-align: center;">
      <p v-if="total === null">
        <span style="text-align: center; color: rgb(246,103,11);">Epoch: </span>
        loading...
      </p>
      <p v-else>
        <span style="text-align: center; color: rgb(246,103,11);">Epoch: </span>
        {{ current }}/{{ total }}
      </p>
    </div>
  </div>
  <div class="progress" role="progressbar" aria-label="Example with label" aria-valuenow="10" aria-valuemin="0"
       aria-valuemax="100">
    <div class="progress-bar" :style="'width: ' + percentage + '%'">{{ percentage }}%</div>
  </div>
</template>


<script setup>
//模拟
// import {onMounted, ref} from "vue";
//
// import {useStore} from 'vuex';
//
// const store = useStore();
// const total = ref(null); // 总数变量
// const percentage = ref(0); // 进度条变量
// const current = ref(0); // 当前值变量
//
// async function epochUpdater() {
//   total.value = 10;
//   current.value = -1;
//   let status = 'running';
//   let step = 100 / total.value;
//   while (percentage.value < 100) {
//     status = 'running';
//     current.value++;
//     percentage.value = Math.min((current.value * step).toFixed(2), 100);
//     if (percentage.value >= 100) {
//       status = 'finish';
//     }
//     await store.dispatch('setStatus2', status);
//     await new Promise(resolve => setTimeout(resolve, 1000)); // 等待1秒钟
//   }
//
// }
//
// onMounted(() => {
//   epochUpdater();
// });

// //正式版
import {inject, onBeforeUnmount, onMounted, ref} from "vue";
import axios from "axios";
import { useStore } from 'vuex';
import Cookies from "js-cookie";

let demoApi = inject('demoApi');
const store = useStore();
let isRefinery = ref(store.getters.getIsRefinery);
let current = ref(null); // 请求到的当前的Epoch
let total = ref(null); // 请求到的该模型总共需要的Epoch
let percentage = ref(0); // 进度条变量
let epochUpdaterInterval; // 请求Epoch轮询控制变量
if(isRefinery.value===true){
  localStorage.setItem('isRefinery', isRefinery.value);
}
if(localStorage.getItem('isRefinery')!==undefined){
  isRefinery.value = localStorage.getItem('isRefinery');
}

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
    clearInterval(epochUpdaterInterval);
  });
}
// 请求epoch轮询函数
const epochUpdater = () => {
  axios
      .get(demoApi.value+'/demo/progress/slm/check', {
        params: {
          taskId:Cookies.get('taskId'),
          isRefinery:isRefinery.value
        }
      })
      .then(response => {
        console.log(response.data)
        if (response.data.code === 200) {
          store.dispatch('setStatus2', response.data.data.status);
          current.value = response.data.data.current;
          // 停止轮询的条件
          if (response.data.data.status === 'finish') {
            current.value=response.data.data.total;
            clearInterval(epochUpdaterInterval);
            if (response.data.data.exit === 1) {
              clearInterval(epochUpdaterInterval);
              open();
              // if (confirm("异常结束！是否重新进行？")) {
              //
              // } else {
              //
              // }
            }
            // 停止之后开始加载模型训练的数据
            // askForSLMDataInterval = setInterval(askForSLMData, 2000)
          }

          total.value = response.data.data.total;
          let step = 100 / total.value;
          percentage.value = Math.min((current.value * step).toFixed(2), 100);
        } else {
          alert(response.data.code + response.data.message);
          clearInterval(epochUpdaterInterval);
        }

      })
      .catch(error => {
        console.error("请求失败:", error);
        alert("请求失败slm");
        clearInterval(epochUpdaterInterval);
      })
};

onMounted(() => {
  epochUpdaterInterval = setInterval(epochUpdater, 5000)
});


// 清理所有的定时器函数
const clearAllInterval = () => {
  if (epochUpdaterInterval !== null) {
    clearInterval(epochUpdaterInterval)
  }
}

// 在组件卸载前清除所有定时器
onBeforeUnmount(() => {
  clearAllInterval();
  store.dispatch('setStatus2', '');
});

</script>


<style scoped>

</style>