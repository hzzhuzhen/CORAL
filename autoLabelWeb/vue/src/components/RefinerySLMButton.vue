<template>
  <el-button type="primary" id="reslm" style="width: 200px" @click="reToSLMView()">Refinery Labeling from SLM
  </el-button>
</template>


<script setup>
import {inject, onMounted, ref} from "vue";
import {useRouter} from 'vue-router';
import {useStore} from 'vuex';
import axios from "axios";

const store = useStore();

const router = useRouter();
let isRefinery = ref(store.getters.getIsRefinery);
let demoApi = inject('demoApi');
//isRefinery.value = true;

function reToSLMView() {
  const taskId = store.getters.getTaskId;
  console.log(taskId);
  console.log("slmIsRefinery="+isRefinery.value);
  isRefinery.value= true;
  localStorage.setItem('isRefinery', 'true');
  store.dispatch('setIsRefinery', true);
  axios
      .get(demoApi.value+"/demo/slm/refinery", {
        params: {
          taskId: 250//taskId,
         // isRefinery:isRefinery.value
        }
      })
      .then((response) => {
        if (response.data.code === 200) {
          //if (status.value === 'finish') {
          //  clearInterval(intervalId);
          //  setTimeout(() => {
          console.log("slmIsRefinery1=" + isRefinery.value);
              router.push({
                path: '/SLMView',
                // query: {
                //   taskId: taskId,
                //   isRefinery:isRefinery.value
                // }
              });
          //  }, 3000);

         // }
        } else {
          alert("reSlm:"+response.data.code + response.data.message);
          //clearInterval(intervalId);
        }
      })
      .catch((error) => {
        console.error("请求失败:", error);
        alert("请求失败reSlm");
        //clearInterval(intervalId);
      });

}

onMounted(() => {
  document.title = 'Result Display';
});
// onBeforeUnmount(() => {
//   clearInterval(intervalId);
// });

</script>


<style scoped>

</style>