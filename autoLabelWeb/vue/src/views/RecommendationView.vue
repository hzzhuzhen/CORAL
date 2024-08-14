<template>
  <div class="recommendation-container">
    <h2>推荐人工标注初始化样本</h2>

    <el-form :model="form" ref="sampleForm" >
      <el-row v-for="(sample, index) in samples" :key="index" :gutter="10">
        <el-col :span="13">
          <!-- 左边的文本框，展示样本 -->
          <el-form-item :label="`初始化样本${index + 1}:`" label-width="100px">
            <!-- <div class="sample-text" readonly>{{ sample.data }}</div> -->
            <el-input v-model="sample.data" placeholder="" disabled type="textarea" rows="4"></el-input>
          </el-form-item>
        </el-col>

        <el-col :span="10">
          <!-- 右边的文本框，用于输入标注结果 -->
          <el-form-item label-width="0px">
            <el-input v-model="sample.labeling" placeholder="输入标注结果" type="textarea" rows="4"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <!-- 提交按钮 -->
    <el-button type="primary" @click="submitLabels">提交</el-button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      // 模拟的初始化样本数据
      samples: [
        { data: '样本1', labeling: '', taskId: 1, id: 101, seq: 1, status: 0 },
        { data: '样本2', labeling: '', taskId: 1, id: 102, seq: 2, status: 0 },
        { data: '样本3', labeling: '', taskId: 1, id: 103, seq: 3, status: 0 },
        { data: '样本4', labeling: '', taskId: 1, id: 104, seq: 4, status: 0 },
        { data: '样本5', labeling: '', taskId: 1, id: 105, seq: 5, status: 0 }
      ],
      form: {
        // 在这里定义表单数据，如果有其他字段，也在这里添加
      }
    };
  },
  methods: {
    submitLabels() {

      const { taskId1} = this.$route.query;
      // 获取表单数据
      const formData = this.samples.map(sample => ({
        data: sample.data,
        labeling: sample.labeling,
        taskId: taskId1,
        id: sample.id,
        seq: sample.seq,
        status: sample.status,
        // 其他字段从this.form中取值，例如：
        // field1: this.form.field1,
        // field2: this.form.field2,
        // ... 其他字段
      }));

      // 使用axios进行POST请求
      axios.post('/manual/labeling/init/save', formData)
        .then(response => {
          // 处理成功的回调
          console.log('提交成功:', response.data);
          this.$router.push('/listtask');
        })
        .catch(error => {
          // 处理失败的回调
          console.error('提交失败:', error);
        });
    }
  }
};
</script>

<style scoped>
.recommendation-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.sample-text {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f5f5f5;
  margin-right: 10px;
}

.label-input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.el-button {
  margin-top: 20px;
}
</style>
