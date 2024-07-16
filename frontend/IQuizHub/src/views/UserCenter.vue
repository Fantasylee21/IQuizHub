<script setup lang="ts">
import UserIntroduction from '@/components/userCenter/UserIntroduction.vue'
import ExerciseRecord from '@/components/userCenter/ExerciseRecord.vue'
import ExerciseContent from '@/components/userCenter/ExerciseContent.vue'
import { ref } from 'vue';
const tabPosition = ref('top');
</script>

<template>

  <el-tabs :tab-position="tabPosition" style="height: 200px;">
    <el-tab-pane label="自我评价">
      <div class="block">
        <UserIntroduction />
      </div>
    </el-tab-pane>
    <el-tab-pane label="题目记录">
    <div class="block">
        <ExerciseRecord />
    </div>
    </el-tab-pane>

  </el-tabs>


</template>

<style scoped>
.block {
  margin: 20px;
  max-width: 800px;
  background: #dee8f3;
  padding: 20px;
}
</style>