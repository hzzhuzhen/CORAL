<template>
  <el-table :data="tableData" border style="width: 100%" class="table-container" :row-style="{ height: '50px' }"
            v-loading="loading" :empty-text="emptyText" element-loading-text="Running...">
    <el-table-column prop="id" label="ID" :min-width="60"/>
    <el-table-column prop="Content" label="Content" show-overflow-tooltip="true" :min-width="240">
      <template v-slot="scope">
        <div class="table-cell">
          <strong>{{ scope.row.content }}</strong>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="LLMLabel" label="LLM Label" :min-width="85">
      <template v-slot="scope">
        <div class="table-cell">
          <strong>{{ scope.row.llmLabel }}</strong>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="SLMLabel" label="SLM Label" :min-width="85">
      <template v-slot="scope">
        <div :style="{ color: getColorByRanking(scope.row.gaussianRanking), textAlign: 'center' }">
          <strong>{{ scope.row.slmLabel }}</strong>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="Ranking" sortable label="Gaussian Ranking" :min-width="120">
      <template v-slot="scope">
        <div :style="{ color: getColorByRanking(scope.row.gaussianRanking), textAlign: 'center' }">
          <strong>{{ scope.row.gaussianRanking }}</strong>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="Confidence" sortable label="Confidence" :min-width="130">
      <template v-slot="scope">
        <div :style="{ color: getColorByRanking(scope.row.gaussianRanking), textAlign: 'center' }">
          <strong>{{ scope.row.confidence }}</strong>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <div class="block-container" >
    <!--    <span class="demonstration">直接前往</span>-->
    <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        v-model:currentPage="currentPage"
        :page-size="1"
        layout="prev, pager, next, jumper"
        :total="lastPage">
    </el-pagination>
  </div>

</template>


<script setup>
import {computed, inject, onBeforeUnmount, ref} from "vue";
import axios from "axios";
import {useStore} from 'vuex';
import Cookies from "js-cookie";

let demoApi = inject('demoApi');
const store = useStore();
let currentPage = ref(1);
let status = ref(store.getters.getStatus2);
let loading = ref(true); // 是否加载控制变量
let tableData = ref([]);
//let isRefinery = inject('isRefinery');
let isRefinery = ref(store.getters.getIsRefinery);
let lastPage=ref(1);
let page=ref(1);
// let interval;
// let labelMatch=ref(0);

if(isRefinery.value===true){
  localStorage.setItem('isRefinery', isRefinery.value);
}
if(localStorage.getItem('isRefinery')!==undefined){
  isRefinery.value = localStorage.getItem('isRefinery');
}

const emptyText = computed(() => {
  return loading.value ? 'Loading Data...' : 'no data';
});
const handleSizeChange = (val) => {
  console.log(`每页 ${val} 条`);
}
const handleCurrentChange = (val) => {
  console.log(`当前页: ${val}`);
  updateForm();
}
const getColorByRanking = (ranking) => {
  if (ranking < 50) {
    return 'rgb(3,182,21)';
  } else if (ranking > 8000) {
    return 'red';
  } else {
    return 'black';
  }
};

// const getLabelMatch=()=>{
//   if(status.value==='finish'){
//     labelMatch.value=ref(store.getters.getLabelMatch);
//     clearInterval(interval);
//   }
// }

const intervalId = setInterval(() => {
  loading.value = true;
  status.value = store.getters.getStatus2;
  // 只有当进度条为100时，表格才会有结果
  if (status.value === 'finish') {
    clearInterval(intervalId);
    updateForm();
  }
}, 2000);
//http://26.112.253.186:8082/demo/progress/slm/check/form
const updateForm = () => {
  page.value=currentPage.value;
  axios
      .get(demoApi.value+"/demo/progress/slm/check/form", {
        params: {
          taskId:Cookies.get('taskId'),
          page: page.value,
          size: 40,
          isRefinery:isRefinery.value
        }

      })
      .then((response) => {
        console.log(response.data.code);
        if (response.data.code === 200) {
          //console.log(isRefinery.value);
          loading.value = false;
          store.dispatch('setLoading', loading);
          //分页处理
          lastPage.value = response.data.data.lastPage;

        //store.dispatch('setTableData', tableData);


          //填充表格
          tableData.value = [];
          const content1 = response.data.data.content;
          const content2 = JSON.parse(content1);
          for (const item of content2) {
            tableData.value.push({
              id: item.id,
              content: item.content,
              llmLabel: item.llmLabel,
              slmLabel: item.slmLabel,
              gaussianRanking: item.ranking,
              confidence: item.confidence
            });
          }

        } else {
          alert("slmForm:" + response.data.code + response.data.message);
        }
      })
      .catch(error => {
        console.error(error);
      });

}

// onMounted(() => {
//    interval = setInterval(getLabelMatch, 5000);
// //
// //   if(status.value==='finish'){
// //     clearInterval(intervalId);
// //     updateForm();
// //   }
//  });

onBeforeUnmount(() => {
  clearInterval(intervalId);
  //clearInterval(interval); // 组件卸载前清除定时器
  store.dispatch('setLoading', true);
  //tableData.value = [];
});
</script>


<style scoped>
.table-container {
  margin-top: 10px;
  /* display: flex; */
  justify-content: center;
  height: 540px;
  /* 设置容器的固定高度 */
  overflow-y: scroll;
  /* 添加垂直滚动条 */
}
.block-container {
  display: flex;
  justify-content: center; /* 水平居中 */
}
</style>