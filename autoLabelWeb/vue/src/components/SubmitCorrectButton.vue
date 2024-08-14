<template>
  <el-button type="primary" style="width: 200px" @click="modifyLabelAndSubmit">
    Submit Correct Label
  </el-button>
</template>
<script setup props="props">
import axios from "axios";
import {inject} from "vue";
import {eventBus} from "@/main";

let demoApi = inject('demoApi');

const modifyLabelAndSubmit= async () => {
  await axios
      .get(demoApi.value+'/demo/manual/label/update')
      .then((response)=>{
        if(response.data.code===200){
          eventBus.emit('updateForm2');
          console.log(response);
        }else{
          console.log(response.data.code+response.data.message);
        }
      })
      .catch((error)=>{
        console.log(error);
      })
}


</script>

<style scoped>

</style>