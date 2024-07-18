<script setup lang="ts">
import { ref } from 'vue'
const tableData = ref([
  {
    date: '2016-05-02',
    name: '超级离散数学三大战python',
    id: '122',
    count: '100',
    favor: '100',
    description: '这是一场超级离散数学三大战python的比赛，题目难度适中，适合大一大二的学生参加'
  }
])

function handleClick() {
  console.log('click')
}
</script>

<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column fixed prop="id" label="ID" width="100" />
    <el-table-column prop="date" label="Date" width="150" />
    <el-table-column prop="name" label="Name" width="300" />
    <el-table-column prop="count" label="题目数" width="120" />
    <el-table-column prop="favor" label="收藏人数" width="120" />
    <el-table-column prop="description" label="Description" width="1000px"/>
    <el-table-column fixed="right" label="Operations" width="120">
      <template #default>
        <el-button link type="primary" size="large" @click="handleClick">
          Try it
        </el-button>
        <el-button link type="primary" size="large">Edit</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<style scoped>

</style>