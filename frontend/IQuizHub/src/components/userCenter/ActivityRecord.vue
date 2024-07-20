<script setup lang="ts">
import { ref } from 'vue'
import { List } from '@element-plus/icons'

const icon = ref({
  type: 'el-icon-chat-line-round',
  color: '#8eb0e4'
});
const tableData = ref([
  {
    date: '2021-09-01',
    name: '第一题',
    type: '选择题',
    behavior: 'right'
  },
  {
    date: '2021-09-02',
    name: '第二题',
    type: '填空题',
    behavior: 'wrong'
  },
  {
    date: '2021-09-03',
    name: '第三题',
    type: '判断题',
    behavior: 'upload'
  },
  {
    date: '2021-09-04',
    name: '第四题',
    type: '选择题',
    behavior: 'right'
  }
]);
const username = ref('admin');

</script>

<template>
  <h2>活动记录 <el-icon size="22px"><List /></el-icon></h2>
  <div class="block" v-for="item in tableData" :key="item.date">
    <el-timeline >
        <el-timeline-item :timestamp="item.date" :color="icon.color" placement="top">
          <el-card shadow="always" class="card">
            <p v-if="item.behavior ==='right'">{{username}} 做对了{{ item.name }}，这是一道{{ item.type }}</p>
            <p v-if="item.behavior ==='wrong'">{{username}} 完成了{{ item.name }}，这是一道{{ item.type }}，但是答错了</p>
            <p v-if="item.behavior ==='upload'">{{username}} 上传了{{ item.name }}，这是一道{{ item.type }}</p>
          </el-card>
        </el-timeline-item>
    </el-timeline>
  </div>
</template>

<style scoped>
h2 {
  font-size: 25px;
  margin: 30px 30px 30px 0;
}

.card{
  color: #121212;
  font-size: 18px;
}

.card:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
}

</style>