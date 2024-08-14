<template>
  <el-button type="primary" id="rellm" style="width: 200px" @click="reToLLMView()">Refinery Labeling from LLM
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
//let status = ref(store.getters.getStatus);


// const intervalId = setInterval(() => {
//   status.value = store.getters.getStatus;
// }, 2000);

function reToLLMView() {
  const taskId = store.getters.getTaskId;
  console.log(taskId);
  console.log("llmisRefinery=" + isRefinery.value);
  // 存储
  localStorage.setItem('isRefinery', 'true');
  console.log("isRefinery2222=" + localStorage.getItem("isRefinery"));

  store.dispatch('setIsRefinery', true);
  axios
      .get(demoApi.value + "/demo/llm/refinery", {
        params: {
          taskId: 250//taskId,
          //isRefinery:isRefinery.value
        }
      })
      .then((response) => {
        if (response.data.code === 200) {
          console.log("reLlm.code=" + response.data.code);
          router.push({
            path: '/LLMView',
            //query: isRefinery
          });
        } else {
          //alert("next:"+response.data.code + response.data.message);
          // clearInterval(intervalId);
        }
      })
      .catch((error) => {
        console.error("请求失败:", error);
        alert("请求失败reLlm");
        // clearInterval(intervalId);
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