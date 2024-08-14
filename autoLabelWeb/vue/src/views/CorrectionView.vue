<template>
  <ContentBase>
    <div class="button-container" style="margin-bottom: 10px;">
      <button id="csv2user">模版导出</button>
      <input type="file" id="csvFileInput" accept=".csv" style="display: none;">
      <button id="user2sys">人工标注导入</button>
    </div>

    <form @submit.prevent="submitManual">
      <div class="table-container">
        <table>
          <thead>
          <tr>
            <th>ID</th>
            <th>Content</th>
            <th>LLM Label</th>
            <th>SLM Label</th>
            <th>Metric 1</th>
            <th>Metric 2</th>
            <th>Metric 3</th>
            <th>Manual Label</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="item in backendData" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.data }}</td>
            <td>{{ item.llmLabel }}</td>
            <td>{{ item.slmLabel }}</td>
            <td>{{ item.loss }}</td>
            <td>{{ item.representation }}</td>
            <td>{{ item.confidence }}</td>
            <td>
              <input type="text" v-model="item.manualLabel"/>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
      <div>
        <button type="submit" style="margin-top: 10px;">提交</button>
      </div>
    </form>
  </ContentBase>
</template>

<script setup>
import ContentBase from '../components/ContentBase';
import {onMounted, ref} from 'vue';
import $ from 'jquery';
import axios from "axios";
import {useRoute} from 'vue-router';

const route = useRoute();
const taskId = route.query.taskId;
const currentEpoch = route.query.currentEpoch;
let backendData = ref([]);
// 接口23
$.ajax({
  url: 'http://localhost:8082/manual/labeling/correcting/recommend',
  type: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({
    taskId: taskId,
    currentEpoch: currentEpoch
  }),
  success(resp) {
    backendData.value = resp.data;
    // console.log(taskInfo.value);
  }
});
onMounted(() => {
  $('#csv2user').click(function () {
    var table = document.querySelector('.table-container table');
    if (!table) return;
    var csvContent = "data:text/csv;charset=utf-8,";
    // 处理表头
    var headers = [];
    var headerCells = table.querySelectorAll('thead th');
    headerCells.forEach(function (cell) {
      headers.push(cell.innerText);
    });
    csvContent += '"' + headers.join('","') + '"\n';
    // 处理表格内容
    backendData.value.forEach(function (item) {
      var rowData = Object.values(item);
      rowData.forEach(function (value, index) {
        if (typeof value === 'string') {
          rowData[index] = '"' + value.replace(/"/g, '""') + '"';
        }
      });
      csvContent += rowData.join(',') + '\n';
    });
    // 创建并下载 CSV 文件
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "dataset.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });

  $('#user2sys').click(function () {
    $('#csvFileInput').click();
  });

  $('#csvFileInput').change(function (e) {
    var file = e.target.files[0];
    if (file) {
      var reader = new FileReader();

      reader.onload = function (event) {
        var csvData = event.target.result;
        var rows = csvData.split('\n');

        for (var i = 0; i < rows.length; i++) {
          var fields = rows[i].split(',');
          // fields.forEach(function (value, index) {
          //     if (typeof value === 'string') {
          //         fields[index] = '"' + value.replace(/"/g, '""') + '"';
          //     }
          // });

          // 处理每一行的字段
          console.log('行', i + 1, '的字段:', fields);
        }
      };

      reader.readAsText(file, 'UTF-8');
    }
  });
});
const submitManual = () => {
  // 接口24
  var dataArray = [];
  backendData.value.forEach(function (item) {
    var newItem = {
      id: item.id,
      data: item.data,
      llmLabel: item.llmLabel,
      slmLabel: item.slmLabel,
      loss: item.loss,
      representation: item.representation,
      confidence: item.confidence,
      manualLabel: item.manualLabel,
      taskId: taskId,
      currentEpoch: currentEpoch
    };
    dataArray.push(newItem);
  });
  axios.post('http://localhost:8082/manual/labeling/correcting/submit', dataArray)
      .then(response => {
        console.log('服务器响应:', response.data);
        // 处理服务器响应，跳转到下一步或其他操作
        // this.$router.push("/recommend");
      })
      .catch(error => {
        console.error('请求失败:', error);
        // 处理请求失败的情况，提示用户或其他操作
      });
}

</script>
<style scoped>
.whole-div {
  height: auto;
}

.button-container {
  display: flex;
  justify-content: flex-end;
}

.table-container {
  display: flex;
  justify-content: center;
}

.button-container button + button {
  margin-left: 30px;
  /* 设置按钮之间的左边距 */
}

table {
  border-collapse: collapse;
}

th,
td {
  border: 1px solid black;
  padding: 8px;
}
</style>