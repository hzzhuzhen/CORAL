<template>
  <div v-for="person in persons" :key="person.name">
    {{ person.name }} - {{ person.age }}
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import axios from "axios";

const persons = ref([
  {name: 'Alice', age: 30},
  {name: 'Bob', age: 25},
  // more persons
]);

const test = () => {
  axios
      .get("http://26.112.253.186:5000/test", {
        params: {
          page: 1,
          size: 20
        }
      })
      .then(response=>{

        console.log("成功"+response.data.code);
      })
      .catch(error=>{
        console.error(error);
      })
}
onMounted(() => {
  test();
});

</script>

<style scoped>
/* 使用 `<style scoped>` 来编写组件的样式 */
body {
  font-family: Arial, sans-serif;
  margin: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}
</style>