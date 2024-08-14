<template>
  <div class="row">
    <el-steps style="max-width: 1000px; text-align: center"
              :active="step" align-center finish-status="wait"
              process-status="success" simple>
      <el-step title="Task Configuration" style="min-width: 300px;"/>
      <el-step title="LLM Labeling"/>
      <el-step title="SLM Filtering"/>
      <!--<el-step :title="active1"/>-->
      <el-step title="Result Display" style="max-width: 130px;"/>
    </el-steps>
  </div>
</template>

<script setup>
import {defineProps, ref} from 'vue';

const props = defineProps({
  active: {
    type: Number,
    required: true
  }
})
let step = ref(props.active)
</script>

<style scoped>

</style>