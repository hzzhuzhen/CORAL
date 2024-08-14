<template>
  <div ref="chart" :style="chartStyle"></div>
</template>

<script setup>
import {ref, onMounted, onBeforeUnmount, defineProps, watch} from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  options: {
    type: Object,
    required: true
  },
  width: {
    type: String,
    required: true
  },
  height: {
    type: String,
    required: true
  }
});

const chart = ref(null);
let chartInstance = null;
let chartStyle = {
  width: props.width,
  height: props.height
}

onMounted(() => {
  chartInstance = echarts.init(chart.value);
  chartInstance.setOption(props.options);
});

watch(
    () => props.options,
    (newOptions) => {
      if (chartInstance) {
        chartInstance.setOption(newOptions);
      }
    },
    { deep: true }
);

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose();
  }
});
</script>

<style scoped>
/* 这里可以添加组件的样式 */
</style>