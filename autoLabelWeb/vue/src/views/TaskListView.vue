<template>
  <div class="task-list-container">
    <h2>任务列表</h2>

    <!-- 搜索表单 -->
    <el-form :model="searchForm" class="search-form" inline>
      <el-form-item label="任务ID">
        <el-input v-model="searchForm.id" />
      </el-form-item>

      <el-form-item label="任务名称">
        <el-input v-model="searchForm.name" />
      </el-form-item>

      <el-form-item label="任务类型">
        <el-input v-model="searchForm.taskType" />
      </el-form-item>

      <el-form-item label="任务状态">
        <el-input v-model="searchForm.status" />
      </el-form-item>

      <el-form-item label="开始时间">
        <el-input v-model="searchForm.createTime" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="searchTasks">搜索</el-button>
      </el-form-item>
    </el-form>

    <!-- 任务列表表格 -->
    <el-table :data="tasks" stripe style="width: 100%">
      <el-table-column prop="id" label="任务ID"></el-table-column>
      <el-table-column prop="name" label="任务名称"></el-table-column>
      <el-table-column prop="taskType" label="任务类型"></el-table-column>
      <el-table-column prop="status" label="任务状态"></el-table-column>
      <el-table-column prop="createTime" label="开始时间"></el-table-column>
      <el-table-column prop="updateTime" label="结束时间"></el-table-column>
      <el-table-column label="操作" width="200">
        <template v-slot="scope">
          <div class="action-buttons">
            <el-button type="primary" @click="startTask(scope.row.id)">开始</el-button>
            <el-button type="danger" @click="endTask(scope.row.id)">结束</el-button>
            <el-button @click="viewTask(scope.row.id)">查看</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      searchForm: {
        id: null,
        name: null,
        taskType: null,
        status: null,
        createTime: null,
      },
      tasks: [],
    };
  },
  methods: {
    searchTasks() {
      axios
        .get("/task/list", { params: this.searchForm })
        .then((response) => {
          this.tasks = response.data.data;
        })
        .catch((error) => {
          console.error("请求失败:", error);
        });
    },
    startTask(taskId) {
      console.log("开始任务:", taskId);
    },
    endTask(taskId) {
      console.log("结束任务:", taskId);
    },
    viewTask(taskId) {
      var url = '/trackboard/?taskId=' + encodeURIComponent(taskId);
      window.location.href = url;
    },
  },
};
</script>

<style scoped>
.task-list-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.search-form {
  margin-bottom: 20px;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
}
</style>
