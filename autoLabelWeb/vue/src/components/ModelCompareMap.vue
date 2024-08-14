<template>
  <div style="margin-top: 1px; font-size: 25px;">
    <strong>
      {{ title }}
      <!--T-SNE Visualization of Data Distribution-->
    </strong>
  </div>
  <div style="margin-top: 1px;">
    <div style="display: flex; margin-top: 1px; justify-content: center; align-items: center; ">
      <EchartsComponent :options="chartScatter" width="250px" height="250px"/>
      <EchartsComponent :options="chartPie" width="250px" height="250px"/>
    </div>
  </div>
</template>

<script setup>
import {ref, defineProps, onMounted, onBeforeUnmount} from "vue";
import EchartsComponent from "@/components/EchartsComponent.vue";
import {inject} from "vue";
import axios from "axios";
import {useStore} from 'vuex';

const store = useStore();
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  // labelMatch: {
  //   type: String,
  //   required: true
  // }
})

let interval;
let title = ref(props.title)
let labelMatch = ref(0);//ref(props.labelMatch)
let demoApi = inject('demoApi');
let status = ref(store.getters.getStatus2);
let isLoading=ref(true);
let loading=ref(true);
let pieSameData = ref(0);
let pieDifferentData = ref(0);

// function updatePieData(sameValue, differentValue) {
//   this.$emit('updateSamePieData', sameValue);
//   this.$emit('updateDifferentPieData', differentValue);
// }

const pieData = () => {
  status.value = store.getters.getStatus2;
  loading.value=store.getters.getLoading;
  isLoading.value=store.getters.getIsLoading;
  console.log("isLoading11111="+isLoading.value);
  console.log("Loading11111="+loading.value);

  if ((status.value === 'finish' && loading.value===false)||isLoading.value===false) {
    axios
        .get(demoApi.value + '/demo/map/pie')
        .then((response) => {
          if (response.data.code === 200) {
            pieSameData.value = response.data.data.same;
            pieDifferentData.value = response.data.data.Different;
            console.log("same11=" + pieSameData.value);
            chartPie.value.series[0].data = [
              {value: pieSameData.value, name: 'same', itemStyle: {color: '#5470c6'}},
              {value: pieDifferentData.value, name: 'Different ', itemStyle: {color: '#c94f4f'}}
            ];
            labelMatch.value =Math.round( pieSameData.value * 1.0 / (pieSameData.value + pieDifferentData.value) * 100)+'%';
            chartPie.value.title.text = labelMatch.value;

          }
        })
        .catch((error) => {
          console.error("请求失败pie:", error);
        });
    clearInterval(interval);
    //store.dispatch('setIsLoading',true);
  }
}


// const same = 93
// const different = 147
// const rate = (same / (same + different) * 100).toFixed(0) + '%'

//坐标图
const chartScatter = ref({
  xAxis: {},
  yAxis: {},
  legend: {
    data: ['LLM', 'LSM'], // 定义图例数据
    top: '10%' // 图例位置
  },
  series: [
    {
      name: "LLM",
      symbolSize: 11,
      data: [
        [10.0, 8.04],
        [8.07, 6.95],
        [13.0, 7.58],
        [9.05, 8.81],
        [10.0, 6.33],
        [14.0, 8.96],
        [6.03, 7.24],
        [12.0, 6.26]
      ],
      type: 'scatter',
      itemStyle: {
        color: 'rgba(220, 66, 66, 0.7)' // 透明红色
      }
    },
    {
      name: "LSM",
      symbolSize: 11,
      data: [
        [12.5, 6.82],
        [9.15, 7.2],
        [11.5, 7.2],
        [3.03, 4.23],
        [12.2, 7.83],
        [2.02, 4.47],
        [1.05, 3.33],
        [4.05, 4.96],
        [12.0, 8.84],
        [7.08, 5.82],
        [5.02, 5.68],
        [11.0, 8.33],
        [14.0, 7.66],
        [13.4, 6.81]
      ],
      type: 'scatter',
      itemStyle: {
        color: 'rgba(86, 140, 192, 0.7)' // 透明蓝色
      }
    }
  ]
});

//饼图
const chartPie = ref({
  title: {
    text: labelMatch,
    left: 'center',
    top: 'center',
    textStyle: {
      fontSize: '24',
      fontWeight: 'bold'
    }
  },
  legend: {
    top: '5%',
    left: 'center'
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      label: {
        show: false,
        position: 'center'
      },
      data: [
        {value: pieSameData.value, name: 'same', itemStyle: {color: '#5470c6'}},
        {value: pieDifferentData.value, name: 'Different ', itemStyle: {color: '#c94f4f'}}
      ],
      startAngle: 0
    }
  ],
})

const fetchData = () => {
  // chartPie.value.series[0].data = [
  //   { value: pieSameData.value, name: 'same', itemStyle: {color: '#5470c6'}},
  //   { value: pieDifferentData.value, name: 'Different ', itemStyle: {color: '#c94f4f'}}
  // ];
  console.log("same=" + pieSameData.value);
}

onMounted(() => {
  fetchData(); // 初始化时获取一次数据
  const intervalId = setInterval(fetchData, 5000); // 每5秒获取一次数据
  interval = setInterval(pieData, 5000);
  //pieData();

  onBeforeUnmount(() => {
    clearInterval(intervalId); // 组件卸载前清除定时器
    clearInterval(interval);
  });
});
</script>

<style scoped>

</style>