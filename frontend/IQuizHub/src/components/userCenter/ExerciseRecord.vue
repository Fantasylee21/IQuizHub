<script setup lang="ts">
import { ref } from 'vue';
const recordType = ref(0);
const tableData = ref([
  {
    date: '2021-09-01',
    name: '第一题',
    type: '选择题'
  },
  {
    date: '2021-09-02',
    name: '第二题',
    type: '填空题'
  },
  {
    date: '2021-09-03',
    name: '第三题',
    type: '判断题'
  }
]);

function clickButton(value: number) {
  recordType.value = value;
}

function openExercise(row: any) {

}

</script>

<template>
        <el-radio-group v-model="recordType">
            <el-radio-button label="0" @click="clickButton(0)">我的练习记录</el-radio-button>
            <el-radio-button label="1" @click="clickButton(1)">我的错题记录</el-radio-button>
            <el-radio-button label="2" @click="clickButton(2)">我的上传记录</el-radio-button>
        </el-radio-group>
        <el-table :data="tableData" style="width: 100%" v-if="recordType === 0">
            <el-table-column prop="date" label="日期" width="180"></el-table-column>
            <el-table-column prop="name" label="题目"></el-table-column>
            <el-table-column prop="type" label="类型" width="180"></el-table-column>
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

</style>