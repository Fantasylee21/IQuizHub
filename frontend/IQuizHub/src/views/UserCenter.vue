<script setup lang="ts">
import UserIntroduction from '@/components/userCenter/UserIntroduction.vue'
import ExerciseRecord from '@/components/userCenter/ExerciseRecord.vue'
import ExerciseContent from '@/components/userCenter/ExerciseContent.vue'
import {ref} from 'vue';
import UserInfo from '@/components/userCenter/UserInfo.vue'
import ActivityRecord from '@/components/userCenter/ActivityRecord.vue'

const tabPosition = ref('top');
</script>

<template>
  <div id="us">
  <el-tabs :tab-position="tabPosition">
    <el-tab-pane label="个人信息" class="tab-pane">
        <div class="block">
          <UserInfo />
        </div>
        <div class="block">
          <UserIntroduction />
        </div>
        <div class="block">
          <ActivityRecord />
        </div>
    </el-tab-pane>
    <el-tab-pane label="题目记录" class="tab-pane">
        <div class="block">
          <ExerciseRecord />
        </div>
    </el-tab-pane>
  </el-tabs>
  </div>
</template>

<style scoped>

.tab-pane {
    display: flex;
    flex-direction: column;
}

.block {
  width: 96%;
  background: #ECF5FF;
  padding: 20px;
  margin: 20px 0 20px 5px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.block:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

#us {
  width: 1200px;
  margin: 0 auto;
}
</style>