<template>
  <el-table :data="tableData" :loading="isLoading" :empty-text="emptyText" border style="width: 100%"
            class="table-container" :header-row-style="{ background: '#f5f7fa' }">
    <el-table-column prop="id" label="ID" width="80" class="custom-header"
                     :header-cell-style="{ background: '#ff9900' }"/>
    <el-table-column prop="content" label="Content" :show-overflow-tooltip="true"
                     header-cell-style="background-color: #ff9900;">
      <template v-slot="scope">
        <div class="table-cell">
          <strong>{{ scope.row.content }}</strong>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="LLMLabel" label="LLM Label" width="180">
      <template v-slot="scope">
        <div :style="{ color: updatedColumn2[scope.$index] === 'labeling..' ? 'rgb(191,191,0)' : 'black' }">
          <strong>{{ updatedColumn2[scope.$index] }}</strong>
          <!-- {{ scope.row.LLMLabel === 0 ? 'neg' : 'pos' }} -->
        </div>
      </template>
    </el-table-column>
    <!-- <el-table-column label="SLM Label" />
    <el-table-column label="Gaussian Ranking" />
    <el-table-column label="Confidence" />
    <el-table-column label="Manual Label">
        <template #default="{ row }">
            <el-select v-if="showOptions === 0" v-model="row.selectedOption" placeholder="Select an option">
                <el-option label="Option 1" value="option1" />
                <el-option label="Option 2" value="option2" />
            </el-select>
        </template>
    </el-table-column> -->
  </el-table>
  <!--  分页处理-->
  <div class="block-container">
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
//import LLMRunningProgress from "@/components/LLMRunningProgress.vue";
import axios from "axios";
import {computed, onBeforeUnmount, onMounted, ref} from "vue";
import {useStore} from 'vuex';
import {inject} from "vue";

let demoApi = inject('demoApi');
const store = useStore();
const updatedColumn2 = ref([]);
let updateColumn2Interval = null;
let tableData = ref([]);
let isLoading = ref(false);
const total = computed(() => store.getters.getTotal);
let currentPage = ref(1);
let lastPage = ref(1);
let page = ref(1);

tableData.value = [];

const emptyText = computed(() => {
  return isLoading.value ? 'Loading Data..' : 'no data';
});

let index = 0;
while (index < total.value) {
  updatedColumn2.value[index] = ""
  index++;
}
index = 0;
updatedColumn2.value[0] = "labeling..";

const handleSizeChange = (val) => {
  console.log(`每页 ${val} 条`);
}
const handleCurrentChange = (val) => {
  console.log(`当前页: ${val}`);
  updateColumn2();
}
const updateColumn2 = () => {
  const taskId = store.getters.getTaskId;
  const status = store.getters.getStatus;

  if (store.getters.getCurrent > 0) {
    page.value = currentPage.value;
    axios
        .get(demoApi.value + "/demo/progress/llm/check/form", {
          params: {
            taskId: taskId,
            page: currentPage.value,
            size: 40,
          }
        })
        .then((response) => {
          console.log(response.data.code);
          if (response.data.code === 200) {
            //分页处理
            lastPage.value = response.data.data.lastPage;

            tableData.value = [];
            const content1 = response.data.data.content;
            const content2 = JSON.parse(content1);
            console.log("id" + content2[0].index);
            // console.log("")
            for (const item of content2) {
              updatedColumn2.value[item.index] = item.llmLabel;
              tableData.value.push({
                id: item.index,
                content: item.content
              });
            }

            if (status === 'finish') {
              clearInterval(updateColumn2Interval);
              console.log("任务已完成");
            }
          }
        })
        .catch((error) => {
          console.error("请求失败:", error);
          //alert("请求失败form");
          //clearInterval(updateColumn2Interval);
          // 在这里处理请求失败的情况，可以提示用户或执行其他操作
        });
  }


};


onMounted(() => {
  updateColumn2Interval = setInterval(updateColumn2, 2000);
  //updateColumn2Interval = setInterval(updateLastPage, 2000);
});

onBeforeUnmount(() => {
  clearInterval(updateColumn2Interval);
  store.dispatch('setStatus', '');
  store.dispatch('setTotal', 0);
  store.dispatch('setCurrent', 0);
  // tableData.value = [];
  // updatedColumn2.value = [];
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