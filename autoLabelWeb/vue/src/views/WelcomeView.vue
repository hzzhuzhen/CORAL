<template>
  <div>
    <h1>Next Page</h1>
    <div>{{ dynamicTags }}</div>
  </div>
</template>

<script>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
export default {
  setup() {
    const router = useRouter();
    let dynamicTags = [];
    let dynamicTags1 = ["pos", "neg"];
    // let dynamicTags1 = ref(["pos", "neg"]);
    let dynamicTags2 =ref(dynamicTags1);
    let dynamicTags3 =ref([]);
    // 在组件挂载后获取路由参数
    onMounted(() => {
      dynamicTags = router.currentRoute.value.query;
      console.log(dynamicTags1);
      console.log(dynamicTags2);  
      dynamicTags3 = ref(Object.values(dynamicTags));
      console.log(dynamicTags3);  
    });

    const options = dynamicTags3.value.map((tag, index) => ({
            label: tag,
            value: String(index), // 将索引转换为字符串
        }));
    console.log(options)

    return {
      dynamicTags,options,dynamicTags1,dynamicTags2
    };
  },
};
</script>
