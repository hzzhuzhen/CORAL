<template>
  <div class="model-settings-container">
    <h2>大模型提示模版设置</h2>

    <el-form :model="form" ref="form" label-width="150px">
      <el-form-item label="选择提示模版库1">
        <el-select v-model="form.selectedTemplate1" placeholder="请选择">
          <el-option v-for="template in templateOptions1" :key="template.value" :label="template.label" :value="template.value"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="提示内容1">
        <el-input type="textarea" :rows="5" placeholder="提示内容" v-model="form.templateContent1"></el-input>
      </el-form-item>

      <el-form-item label="选择提示模版库2">
        <el-select v-model="form.selectedTemplate2" placeholder="请选择">
          <el-option v-for="template in templateOptions2" :key="template.value" :label="template.label" :value="template.value"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="提示内容2">
        <el-input type="textarea" :rows="5" placeholder="提示内容" v-model="form.templateContent2"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm">下一步</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      form: {
        selectedTemplate1: '',
        templateContent1: '',
        selectedTemplate2: '',
        templateContent2: ''
      },
      templateOptions1: [
        { value: '1', label: '模版1_1' },
        { value: '2', label: '模版1_2' },
        // 添加更多模版选项
      ],
      templateOptions2: [
        { value: '1', label: '模版2_1' },
        { value: '2', label: '模版2_2' },
        // 添加更多模版选项
      ]
    };
  },
  methods: {
    submitForm() {
      // 在这里处理表单提交逻辑
      console.log('表单提交:', this.form);

      const { name, taskType} = this.$route.query;
      const formDataForRequest = 
      [
      {
        content: this.form.templateContent1,
        promptType: this.form.selectedTemplate1,
        name: name,
        taskType: taskType,
        taskId: 1
      },
      {
        content: this.form.templateContent2,
        promptType: this.form.selectedTemplate2,
        name: name,
        taskType: taskType,
        taskId: 2
      }
      ]
;


      // 在这里可以发送表单数据到后端
      axios.post('/prompt/list/save', formDataForRequest)
        .then(response => {
          console.log('服务器响应:', response.data);
          // 处理服务器响应，跳转到下一步或其他操作
          this.$router.push("/recommend");
        })
        .catch(error => {
          console.error('请求失败:', error);
          // 处理请求失败的情况，提示用户或其他操作
        });
    }
  }
};
</script>

<style scoped>
.model-settings-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>
