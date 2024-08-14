<template>
  <el-form-item label="recommend">
    <el-switch v-model="sort" @change="handleSortChange"></el-switch>
  </el-form-item>
  <el-table :data="tableData" :loading="isLoading" :empty-text="emptyText" border style="width: 100%"
            class="table-container" :row-class-name="rowStyle" @row-click="handleRowClick" :max-height="600"
            :height="580">
    <el-table-column prop="id" label="ID" :min-width="57"/>
    <el-table-column prop="Content" label="Content" show-overflow-tooltip="true" :min-width="140">
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
    <el-table-column prop="Ranking" sortable label="Gaussian Ranking" :min-width="110">
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
    <!--    人工标注-->
    <el-table-column label="Manual Label" :min-width="130">
      <template #default="{ row }">
        <el-select v-model="row.manualLabel" placeholder="Select a Label" @change="handleLabelChange(row)">
          <el-option v-for="option in options" :key="option.value" :label="option.label"
                     :value="option.value"/>
        </el-select>
      </template>
    </el-table-column>

  </el-table>
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
import {computed, inject, onMounted, ref,onBeforeUnmount} from "vue";
import axios from "axios";
import {useStore} from "vuex";
import {eventBus} from "@/main";

const store = useStore();
let demoApi = inject('demoApi');

let isLoading = ref(true);
let tableData = ref([]);
let currentPage = ref(1);
let lastPage = ref(1);
let page = ref(1);
let sort = ref(false);
let isRefinery = ref(store.getters.getIsRefinery);
//let loading = ref(store.getters.grtLoading);
const handleSortChange = () => {
  updateForm2();
}

console.log("isRefinery=" + isRefinery.value);
if (isRefinery.value === true) {
  localStorage.setItem('isRefinery', isRefinery.value);
}
if (localStorage.getItem('isRefinery') !== undefined) {
  isRefinery.value = localStorage.getItem('isRefinery');
}


//默认所有label都是-1
tableData.value.push({
  label: '-1'
});

const emptyText = computed(() => {
  return isLoading.value ? 'Loading Data...' : 'no data';
});
const handleSizeChange = (val) => {
  console.log(`每页 ${val} 条`);
}
const handleCurrentChange = (val) => {
  console.log(`当前页: ${val}`);
  updateForm2();
}


// 人工标签选项
const options = [
  {
    label: "Select a Label",
    value: null
  },
  {
    label: "positive",
    value: "1"
  },
  {
    label: "negative",
    value: "0"
  }
]

const getColorByRanking = (ranking) => {
  if (ranking < 50) {
    return 'rgb(3,182,21)';
  } else if (ranking > 8000) {
    return 'red';
  } else {
    return 'black';
  }
};
const rowStyle = ({row}) => {
  if (row.Demo === 1) {
    return 'success-row';
  }
  if (row.Cor === 1) {
    return 'fail-row'
  }
  if (row.Diff === 1) {
    return 'warning-row'
  }
};

const updateForm2 = () => {
  page.value = currentPage.value;
  console.log("isRefinery111" + isRefinery.value);
  axios
      .get(demoApi.value + "/demo/progress/slm/check/form", {
        params: {
          taskId: 250,
          page: page.value,
          size: 40,
          sort: sort.value,
          isRefinery: isRefinery.value
        }
      })
      .then((response) => {
        console.log(response.data.code);
        if (response.data.code === 200) {
          //分页处理
          lastPage.value = response.data.data.lastPage;
          isLoading.value=false;
          store.dispatch('setIsLoading', false);
          //填充表格
          tableData.value = [];
          tableData.value.forEach(item => {
            item.label = -1;
          });

          const content1 = response.data.data.content;
          const content2 = JSON.parse(content1);
          for (const item of content2) {
            tableData.value.push({
              id: item.id,
              content: item.content,
              llmLabel: item.llmLabel,
              slmLabel: item.slmLabel,
              gaussianRanking: item.ranking,
              confidence: item.confidence,
              manualLabel: item.manual_label === 1 ? 'positive' : item.manual_label === 0 ? "negative" : null
            });
          }

        } else {
          alert("resultForm:" + response.data.code + response.data.message);
        }
      })
      .catch(error => {
        console.error(error);
      });


}
//人工标注
const handleLabelChange = (row) => {
  axios
      .post(demoApi.value + "/demo/manual/label/save", {
        index: row.id,
        label: row.manualLabel ? row.manualLabel : '-1'
      })
      // .then(()=>{
      //
      // })
      .catch(error => {
        console.error('Error while sending label to backend:', error);
      });
}

onMounted(() => {
  //console.log("isRefinery111="+isRefinery.value);
  eventBus.on('updateForm2', updateForm2);
  updateForm2();
  //this.$emit('formUpdated');
});
onBeforeUnmount(() => {
  store.dispatch('setIsLoading', true);
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