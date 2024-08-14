<template>
  <!-- <ContentBase> -->
  <div class="row whole-div">
    <div class="row">
      <div class="headline-div">
        <div class="headline">
          SLM Filtering
        </div>
      </div>
    </div>
    <model-use-step-bar :active="2"/>

    <!--      进度条组件-->
    <div class="col-md-4 border-end position-relative">
      <task-information/>
      <model-compare-map title="T-SNE Visualization of Data Distribution"  />
      <SLMRunningProgress/>
      <!--      <div style="margin-top: 2px; font-size: 25px;"><strong>SLM Running Progress</strong></div>-->
      <!--      <div style="margin-top: 15px; font-size: 25px;">-->
      <!--        <div style="text-align: center;">-->
      <!--          <p v-if="totalEpoch === null">-->
      <!--            <span style="text-align: center; color: rgb(246,103,11);">Epoch: </span>-->
      <!--            loading...-->
      <!--          </p>-->
      <!--          <p v-else>-->
      <!--            <span style="text-align: center; color: rgb(246,103,11);">Epoch: </span>-->
      <!--            {{ currentEpoch }}/{{ totalEpoch }}-->
      <!--          </p>-->
      <!--        </div>-->
      <!--      </div>-->
      <!--      <div class="progress" role="progressbar" aria-label="Example with label" aria-valuenow="10" aria-valuemin="0"-->
      <!--           aria-valuemax="100">-->
      <!--        <div class="progress-bar" :style="'width: ' + percentage + '%'">{{ percentage }}%</div>-->
      <!--      </div>-->
    </div>


    <div class="col-md-8 position-relative">
      <SlmForm/>

      <!--      <div class="block">-->
      <!--        <span class="demonstration">直接前往</span>-->
      <!--        <el-pagination-->
      <!--            @size-change="handleSizeChange"-->
      <!--            @current-change="handleCurrentChange"-->
      <!--            :current-page.sync="currentPage3"-->
      <!--            :page-size="100"-->
      <!--            layout="prev, pager, next, jumper"-->
      <!--            :total="lastPage.value">-->
      <!--        </el-pagination>-->
      <!--      </div>-->
      <!--      <el-pagination-->
      <!--          background-->
      <!--          layout="prev, pager, next"-->
      <!--          :total="lastPage.value">-->
      <!--      </el-pagination>-->


      <!--      <el-table :data="tableData" border style="width: 100%;" class="table-container" :row-style="{ height: '50px' }"-->
      <!--                v-loading="loading" :empty-text="emptyText" element-loading-text="Running...">-->
      <!--        <el-table-column prop="id" label="ID" :min-width="60"/>-->
      <!--        <el-table-column prop="Content" label="Content" show-overflow-tooltip="true" :min-width="240">-->
      <!--          <template v-slot="scope">-->
      <!--            <div class="table-cell">-->
      <!--              <strong>{{ scope.row.content }}</strong>-->
      <!--            </div>-->
      <!--          </template>-->
      <!--        </el-table-column>-->
      <!--        <el-table-column prop="LLMLabel" label="LLM Label" :min-width="85">-->
      <!--          <template v-slot="scope">-->
      <!--            <div class="table-cell">-->
      <!--              <strong>{{ scope.row.llmLabel }}</strong>-->
      <!--            </div>-->
      <!--          </template>-->
      <!--        </el-table-column>-->
      <!--        <el-table-column prop="SLMLabel" label="SLM Label" :min-width="85">-->
      <!--          <template v-slot="scope">-->
      <!--            <div :style="{ color: getColorByRanking(scope.row.gaussianRanking), textAlign: 'center' }">-->
      <!--              <strong>{{ scope.row.slmLabel }}</strong>-->
      <!--            </div>-->
      <!--          </template>-->
      <!--        </el-table-column>-->
      <!--        <el-table-column prop="Ranking" sortable label="Gaussian Ranking" :min-width="120">-->
      <!--          <template v-slot="scope">-->
      <!--            <div :style="{ color: getColorByRanking(scope.row.gaussianRanking), textAlign: 'center' }">-->
      <!--              <strong>{{ scope.row.gaussianRanking }}</strong>-->
      <!--            </div>-->
      <!--          </template>-->
      <!--        </el-table-column>-->
      <!--        <el-table-column prop="Confidence" sortable label="Confidence" :min-width="130">-->
      <!--          <template v-slot="scope">-->
      <!--            <div :style="{ color: getColorByRanking(scope.row.gaussianRanking), textAlign: 'center' }">-->
      <!--              <strong>{{ scope.row.confidence }}</strong>-->
      <!--            </div>-->
      <!--          </template>-->
      <!--        </el-table-column>-->
      <!--      </el-table>-->
      <!--      <div class="button-container">-->
      <!--        <el-button :disabled="loading" type="primary"-->
      <!--                   id="NextPage" style="width: 200px"-->
      <!--                   :class="{'next-page-grey': loading, 'next-page-blue': !loading}"-->
      <!--        >Next-->
      <!--        </el-button>-->
      <!--      </div>-->
      <NextButton2/>
    </div>
  </div>
  <!-- </ContentBase> -->
</template>

<script setup>
import {ref, onMounted, onBeforeUnmount} from 'vue';//, computed
import $ from 'jquery';
import axios from 'axios';
import {useRouter} from 'vue-router';

import ModelCompareMap from "@/components/ModelCompareMap.vue";
import Cookies from 'js-cookie';
import SLMRunningProgress from "@/components/SLMRunningProgress.vue";
import TaskInformation from "@/components/TaskInformation.vue";
import SlmForm from "@/components/SlmForm.vue";
import NextButton2 from "@/components/NextButton2.vue";
import ModelUseStepBar from "@/components/ModelUseStepBar.vue";


let loading = ref(true); // 是否加载控制变量
//const store = useStore();
// const emptyText = computed(() => {
//   return loading.value ? 'Loading Data...' : 'no data';
// });

let currentEpoch = ref(null); // 请求到的当前的Epoch
let totalEpoch = ref(null); // 请求到的该模型总共需要的Epoch
let percentage = ref(0); // 进度条变量
let totalData = ref([]); // 请求到的所有模型标签数据存放变量
const chart = ref(null);
let tableData = ref([]);
let epochUpdaterInterval; // 请求Epoch轮询控制变量
let askForSLMDataInterval; // 请求小模型训练完成数据轮询的控制变量
// let lastPage = ref(1);


// const getColorByRanking = (ranking) => {
//   if (ranking < 50) {
//     return 'rgb(3,182,21)';
//   } else if (ranking > 8000) {
//     return 'red';
//   } else {
//     return 'black';
//   }
// };


// const csvData = ref([]);
// const updatedColumn2 = ref([]);
// const updatedColumn3 = ref([]);
// const updatedColumn4 = ref([]);

//获取上个页面数据
const router = useRouter();
let raw_dynamicTags = []
raw_dynamicTags = router.currentRoute.value.query;
let dynamicTags = ref(Object.values(raw_dynamicTags));

const labelMap = {};
dynamicTags.value.forEach((tag, index) => {
  // if(index===-1)  index = 0;
  labelMap[index] = tag;
});

// 请求epoch轮询函数
const epochUpdater = () => {
  axios
      .get('http://localhost:8082/task/progress/check', {
        params: {
          taskId: Cookies.get('taskId')
        }
      })
      .then(response => {
        // epoch.value = response.data.currentEpoch
        console.log(response.data)
        currentEpoch.value = response.data.data.currentEpoch
        totalEpoch.value = response.data.data.epoch
        let step = 100 / totalEpoch.value
        percentage.value = Math.min((currentEpoch.value * step).toFixed(2), 100)
        // 停止轮询的条件
        if (currentEpoch.value >= totalEpoch.value) {
          clearInterval(epochUpdaterInterval);
          // 停止之后开始加载模型训练的数据
          askForSLMDataInterval = setInterval(askForSLMData, 2000)
        }
      })
      .catch(error => {
        console.error(error)
        clearInterval(epochUpdaterInterval);
      })
};

// 小模型训练完成后请求训练好的数据函数
const askForSLMData = () => {
  axios.get('http://localhost:8082/slm/result')
      .then(response => {
        console.log(response.data)
        // let statecode = response.data.code;
        if (response.data.code === 200) {
          clearInterval(askForSLMDataInterval);
          loading.value = false;
          totalData.value = response.data.ScatterData;
          let filterResult = response.data.filterResult;
          for (let i = 0; i < filterResult.length; i++) {
            tableData.value.push(filterResult[i])
          }
          // console.log("tableData:", tableData)
        } else if (response.data.code === 201) {
          // 处理响应状态码为201的情况
          // 执行其他操作
          // myPercentage = response.data.data
        }
      })
      .catch(error => {
        console.error(error);
      });
};

// 加载页面数据函数
const loadPageData = () => {
  // 开始轮询检测迭代次数
  epochUpdaterInterval = setInterval(epochUpdater, 2000)
}

onBeforeUnmount(() => {
  if (chart.value) {
    chart.value.dispose();
  }
});

// 清理所有的定时器函数
const clearAllInterval = () => {
  if (epochUpdaterInterval !== null) {
    clearInterval(epochUpdaterInterval)
  }
  if (askForSLMDataInterval !== null) {
    clearInterval(epochUpdaterInterval)
  }
}

onMounted(() => {
  document.title = 'SLM Labeling';
  $('#NextPage').click(function () {
    router.push({path: "/ResultDisplay", query: Object.values(raw_dynamicTags)});
  });
  // 加载页面数据
  loadPageData()
});

// 在组件卸载前清除所有定时器
onBeforeUnmount(() => {
  clearAllInterval();
});

</script>
<style scoped>
.table-cell {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.fixed-width-table {
  table-layout: fixed;
  width: 100%;
}

.fixed-width-cell {
  width: 100px;
  /* 设置你想要的固定宽度 */
  word-wrap: break-word;
  /* 长内容换行显示 */
}

.headline-div {
  border-width: 0px;
  border-bottom-width: 1px;
  border-style: solid;
  border-color: rgba(242, 242, 242, 1);
  margin-bottom: 10px;
}


.headline {
  font-weight: 650;
  font-style: normal;
  font-size: 32px;
  color: #333333;
  text-align: left;
}

.red {
  background-color: red;
}

#canvasContainer {
  position: relative;
}

canvas {
  position: relative;
}

.distance {
  width: 100px;
  height: 30px;
  font-size: 12px;
  padding: 5px 24px;
}

.blue-button {
  background-color: rgb(22, 155, 213);
  color: white;
  width: 200px;
}

.grey-button {
  background-color: rgb(170, 170, 170);
  color: white;
}

.white-button {
  background-color: white;
}

.whole-div {
  height: auto;
  margin-left: 200px;
  margin-right: 200px;
  border-width: 1px;
  border-style: solid;
  border-color: rgba(242, 242, 242, 1);
}

.button-container {
  margin-top: 10px;
  padding-top: 10px;
  display: flex;
  justify-content: space-evenly;
  padding-bottom: 10px;
  border-width: 0px;
  border-top-width: 1px;
  border-style: solid;
  border-color: rgba(242, 242, 242, 1);
}

.search-button {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
  margin-right: 85px;
  /* 调整按钮的右边距 */
}

.search-button button {
  margin-left: 10px;
  /* 调整两个按钮之间的间距 */
}

.input-container {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}

.input-container div {
  flex: 1;
  margin-right: 10px;
}

.table-container {
  margin-top: 10px;
  /* display: flex; */
  justify-content: center;
  height: 540px;
  /* 设置容器的固定高度 */
  overflow-y: scroll;
  /* 添加垂直滚动条 */
}

table {
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ccc;
  padding: 8px;
}

</style>