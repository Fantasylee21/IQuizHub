<template>
    <div class="common-layout">
        <el-container>
            <el-header class="header">
                <GlobalMenu/>
            </el-header>
            <el-container>
                <el-aside :width="!isCollapse ? '64px' : '200px'">
                    <GlobalSidebar @toggleCollapse="toggleCollapse"/>
                </el-aside>
                <el-main class="main-content">Main</el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import GlobalSidebar from "@/components/GlobalComponents/GlobalSidebar.vue";
import GlobalMenu from "@/components/GlobalComponents/GlobalMenu.vue";

const isCollapse = ref(false);

const toggleCollapse = () => {
    isCollapse.value = !isCollapse.value;
};
</script>

<style scoped>
.header {
    border-bottom: 1px solid var(--el-menu-border-color);
}

.common-layout {
    height: 100vh;
    margin: 0 0 0 0 !important;
}

.el-container {
    height: 100%;
}

.el-aside {
    transition: width 0.3s;
}

.main-content {
    flex: 1;
    padding: 20px;
}
</style>
