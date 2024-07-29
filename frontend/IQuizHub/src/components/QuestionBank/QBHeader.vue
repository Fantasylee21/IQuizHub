<template>
    <div class="sheet-editor-header">

        <div class="se-header-container">
            <el-breadcrumb separator="/" class="breadcrumb">
                <el-breadcrumb-item :to="{ path: '/staging' }">staging</el-breadcrumb-item>
                <el-breadcrumb-item>
                    <a href="#">question-bank</a>
                </el-breadcrumb-item>
            </el-breadcrumb>
            <h1>Question Bank</h1>
        </div>
    </div>
</template>

<script setup lang="ts">

</script>

<style scoped>
.sheet-editor-header {
    background-color: #f5f7fa;
    height: 100px;
    margin: 70px 20px 20px;
    border-radius: 20px;
    box-shadow: #595959 0 0 2px;
}

.se-header-container {
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
</style>