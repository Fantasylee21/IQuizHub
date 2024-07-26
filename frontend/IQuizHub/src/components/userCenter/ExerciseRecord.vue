<script setup lang="ts">
import { ref } from 'vue';
import { TrendCharts } from '@element-plus/icons'
const recordType = ref(0);
const tableData = ref([
  {
    date: '2021-09-01',
    name: '第一题',
    type: '选择题',
    behavior: 'right',
    right: 'True'
  },
  {
    date: '2021-09-02',
    name: '第二题',
    type: '填空题',
    behavior: 'wrong',
    right: 'False'
  },
  {
    date: '2021-09-03',
    name: '第三题',
    type: '判断题',
    behavior: 'upload',
    right: 'True'
  },
  {
    date: '2021-09-04',
    name: '第四题',
    type: '选择题',
    behavior: 'right',
    right: 'True'
  }
]);

function clickButton(value: number) {
  recordType.value = value;
}

function openExercise(row: any) {

}

function deleteExercise(row: any) {

}

</script>

<template>
        <h2>我的记录 <el-icon size="23px"><TrendCharts /></el-icon></h2>
        <el-radio-group v-model="recordType">
            <el-radio-button label="0" @click="clickButton(0)">我的练习记录</el-radio-button>
            <el-radio-button label="1" @click="clickButton(1)">我的错题记录</el-radio-button>
            <el-radio-button label="2" @click="clickButton(2)">我的上传记录</el-radio-button>
        </el-radio-group>
        <el-table :data="tableData" style="width: 100%" v-if="recordType === 0">
            <el-table-column prop="date" label="日期" width="180"></el-table-column>
            <el-table-column prop="name" label="题目"></el-table-column>
            <el-table-column prop="type" label="类型" width="180"></el-table-column>
            <el-table-column prop="right" label="是否正确" width="180" ></el-table-column>
            <el-table-column label="操作" width="180">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="openExercise(row)">查看</el-button>
              </template>
            </el-table-column>
        </el-table>
        <el-table :data="tableData" style="width: 100%" v-if="recordType === 1">
            <el-table-column prop="date" label="日期" width="180"></el-table-column>
            <el-table-column prop="name" label="题目"></el-table-column>
            <el-table-column prop="type" label="类型" width="180"></el-table-column>
            <el-table-column label="操作" width="180">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="openExercise(row)">查看</el-button>
              </template>
            </el-table-column>
        </el-table>
        <el-table :data="tableData" style="width: 100%" v-if="recordType === 2">
            <el-table-column prop="date" label="日期" width="180"></el-table-column>
            <el-table-column prop="name" label="题目"></el-table-column>
            <el-table-column prop="type" label="类型" width="180"></el-table-column>
            <el-table-column label="操作" width="180">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="openExercise(row)">查看</el-button>
              </template>
            </el-table-column>
        </el-table>
</template>

<style scoped>
h2 {
  font-size: 24px;
  margin: 20px 30px 30px 0;
}

.el-radio-group {
  margin: 8px;
}

.el-table {
  margin: 20px 0;
}
</style>