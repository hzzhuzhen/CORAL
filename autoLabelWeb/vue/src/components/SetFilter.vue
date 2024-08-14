<template>
  <div>
    <div style="margin-top: 1px;">
      <div style="margin-top: 1px; font-size: 25px;"><strong>Set Filter</strong></div>
      <div class="left-corner-button-container">
        <el-button type="primary" id="defaultButton">Default</el-button>
        <el-button type="success" id="demoButton">Demo Set</el-button>

      </div>
      <div class="left-corner-button-container">
        <el-button type="warning" id="relabelButton">Re-labeling Set</el-button>
        <el-button type="danger" id="correctionButton">Correction Set</el-button>
      </div>
      <div
          style="margin-top: 5px; text-align: left; font-size: 15px; color: black; margin-left: 22px; line-height: 0.55;">
        <!-- ①Green background-color represents the Demo Set <br>
        ②Red background-color represents the Correction Set <br>
        ③High ranking data in green font  <br>
        ④Low ranking data in red font    <br> -->
        <p class="lightgreen-text">* Demo Set in green background-color</p>
        <p class="yellow-text">* Re-labeling Set in yellow background-color</p>
        <p class="red-text">* Correction Set in red background-color</p>
        <p class="lightgreen-text">* High ranking data in green font</p>
        <p class="red-text">* Low ranking data in red font</p>
        <!-- * Demo Set in green background-color<br>
        * Re-labeling Set in yellow background-color<br>
        * Correction Set in red background-color<br>
        * High ranking data in green font<br>
        * Low ranking data in red font<br> -->
      </div>
    </div>
  </div>
</template>
<script setup>

</script>

<style scoped>
.lightgreen-text {
  color: green;
  font-weight: bold;
  //line-height: 1.5; /* 通过调整行高来增加行距 */
  font-size: 13px;
}

.yellow-text {
  color: rgb(225, 159, 66);
  font-weight: bold;
  //line-height: 1.5; /* 通过调整行高来增加行距 */
  font-size: 13px;
}

.red-text {
  /* color: palevioletred; */
  color: rgb(236, 107, 108);
  font-weight: bold;
  //line-height: 1.5; /* 通过调整行高来增加行距 */
  font-size: 13px;
}
</style>