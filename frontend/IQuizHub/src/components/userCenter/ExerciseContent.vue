<script setup lang="ts">
import { ref } from 'vue';

const data = ref(
  {
    imgPath: 'https://pic2.zhimg.com/v2-0dda71bc9ced142bf7bb2d6adbebe4f0_r.jpg?source=1940ef5c',
    answer: 'A',
    myFalseAnswer: 'B'
  }
)
const appear = ref(false);

</script>

<template>
      <h3>题目：</h3>
      <div class = 'picture'>
        <el-image :src="data.imgPath" fit="contain" ></el-image>
      </div>
      <h3>正确答案：</h3>
      <p>{{ data.answer }}</p>
      <h3 v-if="data.myFalseAnswer !== 'RIGHT_ANSWER' "> 我的错误答案：</h3>
</template>

<style scoped>
.picture {
  width: 50%;
  margin: auto;
}
</style>