<template>
    <div class="nav-container">
        <el-menu
                :default-active="activeIndex"
                class="el-menu-demo"
                mode="horizontal"
                :ellipsis="false"
                @select="handleSelect"
        >
            <img
                    style="width: 120px; margin-left: 60px"
                    src="@/assets/logo.png"
                    alt="Element logo"
            />
            <div class="flex-grow"/>
            <el-menu-item index="0">Processing Center</el-menu-item>
            <el-sub-menu index="1">
                <template #title>Workspace</template>
                <el-menu-item index="2-1">item one</el-menu-item>
                <el-menu-item index="2-2">item two</el-menu-item>
                <el-menu-item index="2-3">item three</el-menu-item>
                <el-sub-menu index="2-4">
                    <template #title>item four</template>
                    <el-menu-item index="2-4-1">item one</el-menu-item>
                    <el-menu-item index="2-4-2">item two</el-menu-item>
                    <el-menu-item index="2-4-3">item three</el-menu-item>
                </el-sub-menu>
            </el-sub-menu>
        </el-menu>
    </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue'

const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
</script>

<style>
.nav-container {
    margin: 0 auto;
    width: 1200px;
}

.flex-grow {
    flex-grow: 1;
}
</style>