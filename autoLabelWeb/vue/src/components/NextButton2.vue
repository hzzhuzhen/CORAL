<template>
  <div class="button-container">
    <el-button
        :disabled="loading&&status.value!=='finish'" type="primary"
        id="NextPage" style="width: 200px"
        :class="{'next-page-grey': loading&&status.value!=='finish', 'next-page-blue': !loading&&status.value==='finish'}"
    >Next
    </el-button>
  </div>
</template>


<script setup>
import {useStore} from 'vuex';
import {onBeforeUnmount, onMounted, ref} from "vue";
import $ from "jquery";
import router from "@/router";

const store = useStore();
let status = ref(store.getters.getStatus2);
let loading = ref(store.getters.getLoading);

const intervalId = setInterval(() => {
  status.value = store.getters.getStatus2;
  loading.value = store.getters.getLoading;
}, 2000);

if (status.value === 'finish') {
  clearInterval(intervalId);
}
onMounted(() => {
  document.title = 'SLM Labeling';
  $('#NextPage').click(function () {
    router.push({path: "/ResultDisplay"});
  });
  // 加载页面数据
  //loadPageData();
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