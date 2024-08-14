<template>
  <!-- <ContentBase> -->
  <div class="row whole-div">
    <div class="row">
      <div class="headline-div">
        <div class="headline">
          Result Display
        </div>
      </div>
    </div>
    <model-use-step-bar :active="3"/>
    <div class="col-md-4 border-end position-relative">
      <task-information/>
      <model-compare-map title="Final Result"  />
      <SetFilter/>

<!--      <div>-->
<!--        <div style="margin-top: 0px;">-->
<!--          <div style="margin-top: 0px; font-size: 25px;"><strong>Set Filter</strong></div>-->
<!--          <div class="left-corner-button-container">-->
<!--            <el-button type="primary" id="defaultButton">Default</el-button>-->
<!--            <el-button type="success" id="demoButton">Demo Set</el-button>-->

<!--          </div>-->
<!--          <div class="left-corner-button-container">-->
<!--            <el-button type="warning" id="relabelButton">Re-labeling Set</el-button>-->
<!--            <el-button type="danger" id="correctionButton">Correction Set</el-button>-->
<!--          </div>-->
<!--          <div-->
<!--              style="margin-top: 5px; text-align: left; font-size: 15px; color: black; margin-left: 22px; line-height: 0.55;">-->
<!--            &lt;!&ndash; ①Green background-color represents the Demo Set <br>-->
<!--            ②Red background-color represents the Correction Set <br>-->
<!--            ③High ranking data in green font  <br>-->
<!--            ④Low ranking data in red font    <br> &ndash;&gt;-->
<!--            <p class="lightgreen-text">* Demo Set in green background-color</p>-->
<!--            <p class="yellow-text">* Re-labeling Set in yellow background-color</p>-->
<!--            <p class="red-text">* Correction Set in red background-color</p>-->
<!--            <p class="lightgreen-text">* High ranking data in green font</p>-->
<!--            <p class="red-text">* Low ranking data in red font</p>-->
<!--            &lt;!&ndash; * Demo Set in green background-color<br>-->
<!--            * Re-labeling Set in yellow background-color<br>-->
<!--            * Correction Set in red background-color<br>-->
<!--            * High ranking data in green font<br>-->
<!--            * Low ranking data in red font<br> &ndash;&gt;-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
    </div>
    <div class="col-md-8 position-relative">

<!--      <el-table :data="tableData" :loading="isLoading" :empty-text="emptyText" border style="width: 100%"-->
<!--                class="table-container" :row-class-name="rowStyle" @row-click="handleRowClick" :max-height="600"-->
<!--                :height="580">-->
<!--        <el-table-column prop="id" label="ID" :min-width="57"/>-->
<!--        <el-table-column prop="Content" label="Content" show-overflow-tooltip="true" :min-width="140">-->
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
<!--        <el-table-column prop="Ranking" sortable label="Gaussian Ranking" :min-width="110">-->
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
<!--        <el-table-column label="Manual Label" :min-width="130">-->
<!--          <template #default="{ row }">-->
<!--            <el-select v-model="row.manualLabel" placeholder="Select a Label">-->
<!--              <el-option v-for="option in options" :key="option.value" :label="option.label"-->
<!--                         :value="option.value"/>-->
<!--            </el-select>-->
<!--          </template>-->
<!--        </el-table-column>-->
<!--      </el-table>-->

      <ResultForm/>

    </div>
    <div class="button-container">
<!--      <el-button type="primary" id="rellm" style="width: 200px">Refinery Labeling from LLM</el-button>-->
<!--      <el-button type="primary" id="reslm" style="width: 200px">Refinery Labeling from SLM</el-button>-->
      <RefineryLLMButton/>
      <RefinerySLMButton/>
      <SubmitCorrectButton/>
<!--      <el-button type="primary" style="width: 200px" @click="modifyLabelAndSubmit">{{-->
<!--          buttonText-->
<!--        }}-->
<!--      </el-button>-->
      <DownloadButton/>
<!--      <el-button type="primary" id="csv2user" style="width: 200px">Download</el-button>-->
    </div>

  </div>
</template>

<script setup>
import {ref, onMounted, onBeforeUnmount} from 'vue'
import $ from 'jquery';
import axios from 'axios';
//import {ElMessage} from 'element-plus'
import {useRouter} from 'vue-router';
import ModelUseStepBar from "@/components/ModelUseStepBar.vue";
import TaskInformation from "@/components/TaskInformation.vue";
import ModelCompareMap from "@/components/ModelCompareMap.vue";
import ResultForm from "@/components/ResultForm.vue";

import RefinerySLMButton from "@/components/RefinerySLMButton.vue";
import RefineryLLMButton from "@/components/RefineryLLMButton.vue";
import DownloadButton from "@/components/DownloadButton.vue";
import SetFilter from "@/components/SetFilter.vue";
import SubmitCorrectButton from "@/components/SubmitCorrectButton.vue";

let isLoading = ref(true);
// const emptyText = computed(() => {
//   return isLoading.value ? 'Loading Data...' : 'no data';
// });
//let buttonText = ref('Submit Correct Label');

let tableData = ref([]);
let askForSLMDataInterval;

let totalData = ref([]);
const chart = ref(null);
const router = useRouter();
let raw_dynamicTags = []
raw_dynamicTags = router.currentRoute.value.query;
let dynamicTags = ref(Object.values(raw_dynamicTags));

//const isRefinery=ref(false);


// 人工标签选项
// const options = [
//   {
//     label: "fair",
//     value: "fair"
//   },
//   {
//     label: "positive",
//     value: "positive"
//   },
//   {
//     label: "negative",
//     value: "negative"
//   }
// ]

// const getColorByRanking = (ranking) => {
//   if (ranking < 50) {
//     return 'rgb(3,182,21)';
//   } else if (ranking > 8000) {
//     return 'red';
//   } else {
//     return 'black';
//   }
// };
//
// const rowStyle = ({row}) => {
//   if (row.Demo === 1) {
//     return 'success-row';
//   }
//   if (row.Cor === 1) {
//     return 'fail-row'
//   }
//   if (row.Diff === 1) {
//     return 'warning-row'
//   }
// };

// 提交人工标注到服务器端函数
// const modifyLabelAndSubmit = () => {
//   console.log("tableData")
//   console.log(tableData.value)
//   if (isLoading.value) {
//     ElMessage({
//       message: 'Data is loading - Please wait until the data is loaded.',
//       type: "error"
//     })
//     return
//   }
//   axios
//       .post("http://localhost:8082/manual/labeling/correcting/submit", tableData.value)
//       .then(response => {
//         ElMessage({
//           message: 'Successful submission - Manual label will serve as ground truth to guide the SLM.',
//           type: 'success'
//         })
//         console.log(response)
//       })
//       .catch(error => {
//         console.log(error)
//       })
// };

const askForSLMData = () => {
  axios.get('http://localhost:8082/slm/result')
      .then(response => {
        // console.log(response.data)
        // let statecode = response.data.code;
        if (response.data.code === 200) {
          clearInterval(askForSLMDataInterval);
          isLoading.value = false;
          totalData.value = response.data.ScatterData;
          tableData.value = [];
          let filterResult = response.data.filterResult;

          for (let i = 0; i < filterResult.length; i++) {
            // 给对象配置人工标注数据
            filterResult[i]["manualLabel"] = ""
            filterResult[i]["taskId"] = "1"
            tableData.value.push(filterResult[i])
          }
        } else if (response.data.code === '201') {
          // 处理响应状态码为201的情况
          // 执行其他操作
          // myPercentage = response.data.data
        }
      })
      .catch(error => {
        console.error(error);
        clearInterval(askForSLMDataInterval);
      });
};
onMounted(async () => {
  document.title = 'Result Display';
  //interval = setInterval(getLabelMatch, 5000);

  // $('#rellm').click(function () {
  //   router.push({path: "/LLMView2", query: Object.values(raw_dynamicTags)});
  // });
  //
  // $('#reslm').click(function () {
  //   router.push({path: "/SLMView", query: Object.values(raw_dynamicTags)});
  // });

  $('#finish').click(function () {
    var url = '/CreateTask/';
    window.location.href = url;
  });

  $('#defaultButton').click(function () {
    tableData.value.sort((a, b) => {
      if (a.id < b.id) {
        return -1;
      }
      if (a.id > b.id) {
        return 1;
      }
      return 0;
    });
  });

  $('#demoButton').click(function () {
    tableData.value.sort((a, b) => {
      if (a.Demo > b.Demo) {
        return -1;
      } else if (a.Demo < b.Demo) {
        return 1;
      } else if (a.id < b.id) {
        return -1;
      } else if (a.id > b.id) {
        return 1;
      }
      return 0;
    });
  });
  $('#correctionButton').click(function () {
    tableData.value.sort((a, b) => {
      if (a.Ranking > b.Ranking) {
        return -1;
      }
      if (a.Ranking < b.Ranking) {
        return 1;
      }
      return 0;
    });
  });
  $('#relabelButton').click(function () {
    tableData.value.sort((a, b) => {
      if (a.Diff > b.Diff) {
        return -1;
      }
      if (a.Ranking < b.Ranking) {
        return 1;
      }
      if (a.Ranking < b.Ranking) {
        return -1;
      }
      if (a.Ranking > b.Ranking) {
        return 1;
      }
      return 0;
    });
  });
//下载
//   $('#csv2user').click(function () {
//     const table = document.querySelector('.table-container .el-table__body-wrapper');
//     if (!table) return;
//     let csvContent = "data:text/csv;charset=utf-8,";
//     // 处理表头
//     const headers = [];
//     const headerCells = table.querySelectorAll('.el-table__header th .cell');
//     headerCells.forEach(function (cell) {
//       headers.push(cell.innerText);
//     });
//     csvContent += 'ID,Content,LLM Label,SLM Label,Ranking,Confidence,Manual Label,Final Label' + '\n';
//     // 处理表格内容
//     const rows = table.querySelectorAll('.el-table__row');
//     rows.forEach(function (row) {
//       const rowData = [];
//       const cells = row.querySelectorAll('.cell');
//       cells.forEach(function (cell) {
//         rowData.push(cell.innerText);
//       });
//       let tmps = "";
//       rowData.forEach(function (value, index) {
//         if (typeof value === 'string') {
//           rowData[index] = '"' + value.replace(/"/g, '""') + '"';
//         }
//         if (index === 3) {
//           if (rowData[6].includes('Select a Label')) {
//             tmps = rowData[3];
//           } else {
//             tmps = rowData[6];
//           }
//         }
//       });
//       rowData.push(tmps);
//       if (rowData.length > 0) {
//         const lastElement = rowData[rowData.length - 1];
//         if (typeof lastElement === 'string' && lastElement.includes('Select a Label')) {
//           rowData[rowData.length - 1] = lastElement.replace(/Select a Label/g, '');
//         }
//       }
//       csvContent += rowData.join(',') + '\n';
//     });
//     // 创建并下载 CSV 文件
//     const encodedUri = encodeURI(csvContent);
//     const link = document.createElement("a");
//     link.setAttribute("href", encodedUri);
//     link.setAttribute("download", "dataset.csv");
//     document.body.appendChild(link);
//     link.click();
//     document.body.removeChild(link);
//   });

  askForSLMDataInterval = setInterval(askForSLMData, 2000)
  onBeforeUnmount(() => {
    if (chart.value) {
      chart.value.dispose();
    }
    //clearInterval(interval); // 组件卸载前清除定时器
  });
});

const labelMap = {};
dynamicTags.value.forEach((tag, index) => {
  labelMap[index] = tag;
});


</script>
<style>
.lightgreen-text {
  color: green;
  font-weight: bold;
}

.yellow-text {
  color: rgb(225, 159, 66);
  font-weight: bold;
}

.red-text {
  /* color: palevioletred; */
  color: rgb(236, 107, 108);
  font-weight: bold;
}

.table-cell {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* .text-container {
    overflow: visible;
    white-space: normal;
} */

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

.left-corner-button-container {
  margin-top: 0px;
  margin-left: 10px;
  margin-right: 10px;
  padding-top: 0px;
  display: flex;
  justify-content: space-evenly;
  padding-bottom: 5px;
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
  /* display: flex;
  justify-content: center; */
  height: 600px;
  /* 设置容器的固定高度 */
  overflow-y: scroll;
  /* 添加垂直滚动条 */
}

.table-container:hover {
  background-color: #fff;
}

table {
  border-collapse: collapse;
}

/* th,
td {
    border: 1px solid #ccc;
    padding: 8px;
} */
.highgreen_class {
  background-color: rgb(114, 163, 118);
}

.el-table .warning-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-7);
}

.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-7);
}

.el-table .fail-row {
  --el-table-tr-bg-color: rgb(232, 183, 183);
}


/* .el-table .success-row:hover {
    background-color: var(--el-color-success-light-7);
}  */

.yellow_class {
  background-color: rgb(221, 241, 91);
}

.el-table--striped .el-table__body tr.el-table__row--striped.current-row td,
.el-table__body tr.current-row > td {
  color: #fff;
  background-color: #fff !important;
}

</style>