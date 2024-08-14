<template>
  <el-button type="primary" style="width: 200px" @click="downloadCSV">Download</el-button>
</template>

<script setup>
import axios from "axios";
import {inject} from "vue";

let demoApi = inject('demoApi');
const downloadCSV =async()=> {
  try {
    const response=await axios({
      url:demoApi.value+'/demo/down/result',
      method:'GET',
      responseType:'blob'
    });

    const url=window.URL.createObjectURL(new Blob([response.data]));
    const link=document.createElement('a');
    link.href=url;
    link.setAttribute('download','dataset.csv');//文件名
    document.body.appendChild(link);
    link.click();

    link.remove();
    window.URL.revokeObjectURL(url);
  }catch (error){
    console.log("下载失败");
  }


  // axios
  //     .get(demoApi.value + '/demo/down/result')
  //     // .then((response) => {
  //     //   const table = response.data;
  //     //   if (!table) return;
  //     //   let csvContent = "data:text/csv;charset=utf-8,";
  //     //   // 处理表头
  //     //   const headers = [];
  //     //   const headerCells = table.querySelectorAll('.el-table__header th .cell');
  //     //   headerCells.forEach(function (cell) {
  //     //     headers.push(cell.innerText);
  //     //   });
  //     //   csvContent += 'ID,Content,LLM Label,SLM Label,Ranking,Confidence,Manual Label,Final Label' + '\n';
  //     //   // 处理表格内容
  //     //   const rows = table.querySelectorAll('.el-table__row');
  //     //   rows.forEach(function (row) {
  //     //     const rowData = [];
  //     //     const cells = row.querySelectorAll('.cell');
  //     //     cells.forEach(function (cell) {
  //     //       rowData.push(cell.innerText);
  //     //     });
  //     //     let tmps = "";
  //     //     rowData.forEach(function (value, index) {
  //     //       if (typeof value === 'string') {
  //     //         rowData[index] = '"' + value.replace(/"/g, '""') + '"';
  //     //       }
  //     //       if (index === 3) {
  //     //         if (rowData[6].includes('Select a Label')) {
  //     //           tmps = rowData[3];
  //     //         } else {
  //     //           tmps = rowData[6];
  //     //         }
  //     //       }
  //     //     });
  //     //     rowData.push(tmps);
  //     //     if (rowData.length > 0) {
  //     //       const lastElement = rowData[rowData.length - 1];
  //     //       if (typeof lastElement === 'string' && lastElement.includes('Select a Label')) {
  //     //         rowData[rowData.length - 1] = lastElement.replace(/Select a Label/g, '');
  //     //       }
  //     //     }
  //     //     csvContent += rowData.join(',') + '\n';
  //     //   });
  //     //   // 创建并下载 CSV 文件
  //     //   const encodedUri = encodeURI(csvContent);
  //     //   const link = document.createElement("a");
  //     //   link.setAttribute("href", encodedUri);
  //     //   link.setAttribute("download", "dataset.csv");
  //     //   document.body.appendChild(link);
  //     //   link.click();
  //     //   document.body.removeChild(link);
  //     // })
  //     .catch((error) => {
  //       console.error("下载失败:", error);
  //       alert("下载失败");
  //     })

};


// import { ref, onMounted } from 'vue';
//
// const table = ref(null);
// const headers = ref([]);
//
// const downloadCSV = async () => {
//   if (!table.value) return;
//
//   let allData = getAllData(); // 获取所有数据
//
//   let csvContent = "data:text/csv;charset=utf-8,";
//
//   // 处理表头
//   headers.value.forEach((header, index) => {
//     if (index > 0) {
//       csvContent += ",";
//     }
//     csvContent += '"' + header.innerText + '"';
//   });
//   csvContent += '\n';
//
//   // 处理所有数据
//   allData.forEach((rowData) => {
//     rowData.forEach((cell, index) => {
//       if (index > 0) {
//         csvContent += ",";
//       }
//       csvContent += '"' + cell.toString().replace(/"/g, '""') + '"';
//     });
//     csvContent += '\n';
//   });
//
//   // 创建并下载 CSV 文件
//   const encodedUri = encodeURI(csvContent);
//   const link = document.createElement("a");
//   link.setAttribute("href", encodedUri);
//   link.setAttribute("download", "dataset.csv");
//   document.body.appendChild(link);
//   link.click();
//   document.body.removeChild(link);
// };
//
// const getAllData = () => {
//   let allData = [];
//   if (table.value && table.value.$parent && table.value.$parent.data) {
//     allData = table.value.$parent.data;
//   }
//   return allData;
// };
//
// onMounted(() => {
//   table.value = document.querySelector('.table-container .el-table__body-wrapper');
//   if (table.value) {
//     headers.value = table.value.querySelectorAll('.el-table__header th .cell');
//   }
// });
</script>

<style scoped>

</style>