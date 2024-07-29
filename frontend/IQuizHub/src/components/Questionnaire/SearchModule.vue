<script setup lang="ts">

import { Search } from '@element-plus/icons'
import { ref } from 'vue'
import NaireSheet from '@/components/Questionnaire/NaireSheet.vue'
const searchValue = ref('')
const activeName = ref('first')
const record = ref(123)
function search() {
  console.log('search')
}

function handleClick(tab: any) {
  console.log(tab)
}
</script>

<template>
  <div>
    <div class="search">
    <h2>Search Sheet</h2>
    <div>
      <el-input placeholder="enter the name of the questionnaire" v-model="searchValue" clearable>
          <template #prepend >
            <div class="search-icon-container">
              <el-icon size="23px"><Search /></el-icon>
            </div>
          </template>
      </el-input>
      <el-button type="primary" @click="search">Search</el-button>
    <h3>Sheet Type</h3>
      <div class="result">
      <p>{{record}}</p>
      <h4> results</h4>
      </div>
    </div>
    </div>
    <div class="el-tabs-all">
      <el-tabs
      v-model="activeName"
      type="card"
      class="demo-tabs"
      @tab-click="handleClick"
      >
      <el-tab-pane label="IQuizHub严选" name="first">
        <div class="block">
            <NaireSheet></NaireSheet>
        </div>
      </el-tab-pane>
      <el-tab-pane label="用户上传" name="second">
        <div class="block">
            <NaireSheet></NaireSheet>
        </div>
      </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<style scoped>

h2 {
  font-size: 25px;
  margin-top: 20px;
}

h3 {
  font-size: 20px;
  margin-top: 20px;
}

h4 {
  font-size: 15px;
  margin-top: 10px;
  color: #000000;
}

p {
  font-size: 18px;
  margin-top: 8px;
  margin-left: 10px;
  margin-right: 10px;
  color: #143a77;
}

.result {
  display: flex;
  margin-top: 10px;
  max-width: 200px;
  margin-left: 30px;
}

.result > div {
  flex: 1;
  text-align: center;
}

.search-icon-container {
  width: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.el-input {
  width: 500px;
  margin-top: 30px;
  margin-left: 30px;
  height: 35px;
}

.el-button {
  margin-top: 30px;
  margin-left: 20px;
}

.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.el-tabs-all {
  background: #ECF5FF;
  padding: 20px;

  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin: 40px auto 40px auto;
}

.el-tabs-all:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.search {
  border-width: 1px;
  background: #ECF5FF;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin: 40px auto 40px auto;
}

.search:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
</style>