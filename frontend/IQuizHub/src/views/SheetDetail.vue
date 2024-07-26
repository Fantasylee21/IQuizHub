<template>
    <div class="sheet-detail-header">
        <div class="sd-header-container">
            <el-breadcrumb separator="/" class="breadcrumb">
                <el-breadcrumb-item :to="{ path: '/staging' }">staging</el-breadcrumb-item>
                <el-breadcrumb-item :to="{ path: '/question-sheet' }">question-sheet</el-breadcrumb-item>
                <el-breadcrumb-item>
                    <a href="#">sheet-detail</a>
                </el-breadcrumb-item>
            </el-breadcrumb>
            <h1>题单的名字</h1>
            <div class="info-container">
                <el-button type="primary" @click="collect">收藏题单</el-button>
                <div class="info-statistic" style="display: flex">
                    <el-statistic title="题目总数" :value="15" style="margin-right: 20px"></el-statistic>
                    <el-statistic title="收藏数" :value="1000"></el-statistic>
                </div>

            </div>
        </div>
    </div>
    <div class="sheet-detail-container">

    </div>
</template>

<script setup lang="ts">
const collect = () => {

}
</script>

<style scoped>
.sheet-detail-header {
    background-color: #f5f7fa;
    height: 150px;
    margin: 70px 20px 20px;
    border-radius: 20px;
    box-shadow: #595959 0 0 2px;
}

.sd-header-container {
    width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
}

.breadcrumb {
    margin-top: 20px;
    margin-bottom: 15px;
}

h1 {
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    margin-bottom: .5em;
    font-family: inherit;
    font-weight: bold;
    line-height: 1.2;
    color: inherit;
    font-size: 1.75em;
}

.info-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.sheet-detail-container {
    width: 1200px;
    margin: 0 auto;
}
</style>