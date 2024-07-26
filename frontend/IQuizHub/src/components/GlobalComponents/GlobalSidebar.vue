<template>
    <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            :collapse="isCollapse"
            @open="handleOpen"
            @close="handleClose"
            :router="true"
    >
        <el-menu-item @click="toggleCollapse">
            <el-icon>
                <component :is="isCollapse ? ArrowRight : ArrowLeft"/>
            </el-icon>
            <template #title>Toggle Collapse</template>
        </el-menu-item>
        <el-menu-item index="/staging">
            <el-icon>
                <User/>
            </el-icon>
            <template #title>工作台</template>
        </el-menu-item>
        <el-menu-item index="/groupPage">
            <el-icon>
                <Share/>
            </el-icon>
            <template #title>群组界面</template>
        </el-menu-item>
        <el-menu-item index="/question-sheet">
            <el-icon>
                <icon-menu/>
            </el-icon>
            <template #title>题单广场</template>
        </el-menu-item>
        <el-menu-item index="/questionBank">
            <el-icon>
                <Grid/>
            </el-icon>
            <template #title>题库</template>
        </el-menu-item>
        <el-menu-item index="/userCenter">
            <el-icon>
                <setting/>
            </el-icon>
            <template #title>个人中心</template>
        </el-menu-item>
        <el-menu-item index="/question-editor">
            <el-icon>
                <Edit/>
            </el-icon>
            <template #title>上传题目</template>
        </el-menu-item>
        <el-menu-item index="/test">
            <el-icon>
                <setting/>
            </el-icon>
            <template #title>test</template>
        </el-menu-item>
    </el-menu>
</template>

<script lang="ts" setup>
import {ref, defineEmits} from 'vue';
import {
    Document,
    Menu as IconMenu,
    Location,
    Setting,
    Share
} from '@element-plus/icons-vue';
import {ArrowLeft, ArrowRight} from '@element-plus/icons-vue';
import {Grid} from '@element-plus/icons-vue';
import {Edit, User} from "@element-plus/icons";

const isCollapse = ref(true);
const handleOpen = (key: string, keyPath: string[]) => {
    console.log(key, keyPath);
};
const handleClose = (key: string, keyPath: string[]) => {
    console.log(key, keyPath);
};
const emit = defineEmits(['toggleCollapse']);
const toggleCollapse = () => {
    isCollapse.value = !isCollapse.value;
    emit('toggleCollapse');
};
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}

.el-menu-vertical-demo.el-menu--collapse {
    width: 64px;
}
</style>
