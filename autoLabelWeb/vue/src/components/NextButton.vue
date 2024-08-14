<template>
  <div class="button-container">
    <!-- <button id="NextPage" class="blue-button">
            Next
        </button> -->
    <el-button type="primary" id="NextPage" style="width: 200px" :disabled="status !== 'finish'"
               :class="{'next-page-grey':status!=='finish', 'next-page-blue': status==='finish'}"
               @click="navigateToSLMView">Next
    </el-button>
  </div>
</template>

<script setup>
import {ref, onBeforeUnmount, onMounted, inject} from 'vue';
import router from '@/router';
import {useStore} from 'vuex';
import axios from "axios";
import Cookies from "js-cookie";
const store = useStore();

let isRefinery = ref(store.getters.getIsRefinery);
let demoApi = inject('demoApi');



const apiAdd = isRefinery.value ? '/demo/slm/refinery' : '/demo/slm';
let status = ref(store.getters.getStatus);
const intervalId = setInterval(() => {
  status.value = store.getters.getStatus;
}, 2000);

const navigateToSLMView = () => {
  const taskId = Cookies.get('taskId');
  //const taskId = store.getters.getTaskId;
  console.log("NextIsRefinery=" + isRefinery.value);
  axios
      .get(demoApi.value + apiAdd, {
        params: {
          taskId: taskId,
          // isRefinery: isRefinery.value
        }
      })
      .then((response) => {
        if (response.data.code === 200) {
          clearInterval(intervalId);
          router.push({
            path: '/SLMView',
            // query: Object.values(raw_dynamicTags)
          });
        }
      })
      .catch((error) => {
        console.error("请求失败:", error);
        alert("请求失败next");
        clearInterval(intervalId);
      });
}

onMounted(() => {
  console.log("Initial status value: " + status.value);
});
onBeforeUnmount(() => {
  clearInterval(intervalId);
});


</script>


<style scoped>
.next-page-grey {
  background-color: grey !important;
  border-color: grey !important;
  color: white !important;
}

.next-page-blue {
  background-color: #409EFF !important;
  border-color: #409EFF !important;
  color: white !important;
}
</style>