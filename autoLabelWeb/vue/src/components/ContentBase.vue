<template>
  <div class="home">
    <div class="container">
      <div class="card">
        <div class="card-body">
          <slot></slot>
        </div>
      </div>

    </div>


  </div>
</template>

<script>
export default {
  name: "ContentBase",
}

</script>

<style scoped>
.container {
  margin-top: 20px;
  /* height: 100vh; */
  /* 使用视口高度的 80% */
  width: 100%;
  /* 使用视口宽度的 80% */
}
</style>
