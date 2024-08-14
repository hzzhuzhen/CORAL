<template>
  <el-table :data="tableData" border style="width: 100%;" class="table-container" :row-style="{ height: '50px' }"
            element-loading-text="Running...">
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
        <div :style="{ textAlign: 'center' }">
          <strong>{{ scope.row.slmLabel }}</strong>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="Ranking" sortable label="Gaussian Ranking" :min-width="120">
      <template v-slot="scope">
        <div :style="{ textAlign: 'center' }">
          <strong>{{ scope.row.gaussianRanking }}</strong>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="Confidence" sortable label="Confidence" :min-width="130">
      <template v-slot="scope">
        <div :style="{ textAlign: 'center' }">
          <strong>{{ scope.row.confidence }}</strong>
        </div>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
import {onMounted, ref} from "vue";

const tableData = ref([])

onMounted(() => {
  for (let i = 0; i < 10000; i++) {
    tableData.value.push({
      id: 1,
      content: 'with we were soldiers , hollywood makes a valiant attempt to tell a story about the vietnam war before the pathology set in .',
      llmLabel: 'positive',
      slmLabel: 'positive',
      gaussianRanking: 12,
      confidence: 0.9925
    });
  }
})
</script>

<style scoped>

</style>